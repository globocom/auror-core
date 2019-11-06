import shutil
import tempfile
import os

import mock

from unittest import TestCase

from auror_core.v2.job import Job, Command
from auror_core.v2.loader import Loader


class LoaderTest(TestCase):

    def test_error_on_inexistence_file_path(self):
        with self.assertRaises(ValueError) as context:
            Loader('/this/does/not/exist/flow.yaml')
        self.assertTrue('File does not exists' in str(context.exception))
    
    @mock.patch('auror_core.v2.loader.os')
    @mock.patch('auror_core.v2.loader.yaml')
    @mock.patch('auror_core.v2.loader.open')
    def test_should_return_command_type_job_list(self, mock_os, mock_yaml, mock_open):
        job = {
            'config': {
                'command': 'COMMAND'
            },
            'dependsOn': ['firstDependencie', 'secondDependecie'],
            'name': 'AZTest',
            'type': 'command'
        }
        mock_os.path.exists.return_value = True
        mock_yaml.safe_load.return_value = {'nodes': [job, job]}

        loader = Loader('/flow/path/flow.yaml')
        jobs = loader.as_job_objects()

        self.assertIsInstance(jobs, list)
        self.assertEqual(2, len(jobs))
        self.assertTrue(all([isinstance(job, Job) for job in jobs]))
    
    @mock.patch('auror_core.v2.loader.os')
    @mock.patch('auror_core.v2.loader.yaml')
    @mock.patch('auror_core.v2.loader.open')
    def test_should_return_embbed_flow(self, mock_os, mock_yaml, mock_open):
        job = {
            'config': {
                'command': 'COMMAND'
            },
            'dependsOn': ['firstDependencie', 'secondDependecie'],
            'name': 'AZTest',
            'type': 'command'
        }
        job['nodes'] = [job.copy(),]
        mock_os.path.exists.return_value = True
        mock_yaml.safe_load.return_value = {'nodes': [job,]}

        loader = Loader('/flow/path/flow.yaml')
        jobs = loader.as_job_objects()

        expected_job = Command(
            job['name'],
            job['config'],
            job['dependsOn'],
        ).with_command(job['config']['command'])
        expected_job = expected_job.with_nodes(expected_job)

        self.assertEqual(1, len(jobs))
        self.assertEqual(expected_job, jobs[0])
