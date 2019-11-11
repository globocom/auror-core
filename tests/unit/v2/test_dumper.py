import shutil
import tempfile

import autopep8

from unittest import TestCase

from auror_core.v2.job import Command
from auror_core.v2.dumper import Dumper


class TestDumper(TestCase):
    
    def setUp(self):
        self.tem_dir = tempfile.mkdtemp()
        self.dumper = Dumper(self.tem_dir)
    
    def tearDown(self):
        shutil.rmtree(self.tem_dir)
    
    def test_should_raise_an_exception_on_inexistence_directory(self):
        path = '/this/path/does/not/exist'
        with self.assertRaises(ValueError) as context:
            Dumper(path)
        self.assertTrue(
            'Directory, {}, does not exist'.format(path) in str(context.exception)
        )
    
    def test_dump_simple_job(self):
        simple_job = Command(
            name='shell_pwd',
            config={
                'command': 'pwd'
            }
        )
        expected_file_content = autopep8.fix_code(
            '{}job_0 = {}\n'.format(Dumper.DEFAULT_IMPORTS, repr(simple_job)),
            options={
                'aggressive': True,
            }
        )

        self.dumper.dump_jobs(simple_job)

        with open('{}/flow.py'.format(self.tem_dir)) as _file:
            file_content = ''.join(_file.readlines())
        self.assertEqual(expected_file_content, file_content)
    
    def test_dump_two_jobs(self):
        job = Command(
            name='shell_pwd',
            config={
                'command': 'pwd'
            }
        )
        expected_file_content = autopep8.fix_code(
            '{}job_0 = {}\n\njob_1 = {}\n'.format(Dumper.DEFAULT_IMPORTS, repr(job), repr(job)),
            options={
                'aggressive': True,
            }
        )

        self.dumper.dump_jobs(job, job)
        
        with open('{}/flow.py'.format(self.tem_dir)) as _file:
            file_content = ''.join(_file.readlines())
        self.assertEqual(expected_file_content, file_content)
    
    def test_dump_embbed_job(self):
        internal_job = Command(
            name='shell_pwd',
            config={
                'command': 'pwd'
            }
        )
        embbed_job = Command(
            name='embedded_flow1',
            config={
                'command': 'flow_command',
            },
            nodes=[internal_job,]
        )

        expected_file_content = autopep8.fix_code(
            '{}job_0 = {}\n'.format(Dumper.DEFAULT_IMPORTS, repr(embbed_job)),
            options={
                'aggressive': True,
            }
        )

        self.dumper.dump_jobs(embbed_job)
        
        with open('{}/flow.py'.format(self.tem_dir)) as _file:
            file_content = ''.join(_file.readlines())
        self.assertEqual(expected_file_content, file_content)
    
    def test_dump_one_embbed_job_and_one_simple_job(self):
        job = Command(
            name='shell_pwd',
            config={
                'command': 'pwd'
            }
        )
        embbed_job = Command(
            name='embedded_flow1',
            config={
                'command': 'flow_command',
            },
            nodes=[job,]
        )
        expected_file_content = autopep8.fix_code(
            '{}job_0 = {}\n\njob_1 = {}\n'.format(Dumper.DEFAULT_IMPORTS, repr(job), repr(embbed_job)),
            options={
                'aggressive': True,
            }
        )

        self.dumper.dump_jobs(job, embbed_job)
        
        with open('{}/flow.py'.format(self.tem_dir)) as _file:
            file_content = ''.join(_file.readlines())
        self.assertEqual(expected_file_content, file_content)
