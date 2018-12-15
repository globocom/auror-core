#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil, tempfile
from unittest import TestCase
from auror_core import Project
from auror_core.job import Job, Command
from auror_core.params import Params, Env, ParamsJoin

params = Params(
    "params",
    retries="2",
    **{
        "retry.backoff": "30000",
        "failure.emails": "email@gmail.com"
    }
)

envs = Env(
    "some_envs",
    SOMETHING_KEY = "xxxxxxxx",
    SPARK_MASTER="yarn"
)

job1_command = Job() \
    .as_type(Command) \
    .with_name("job1_command") \
    .with_command("${python} -c 'from test import test_method; test_method()'")


class TestCaseWithNecessaryConditions(TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def list_files(self):
        return os.listdir(self.test_dir)

    def open_file(self, name):
        return open(os.path.join(self.test_dir, name))


class ParamsPropertiesFileTest(TestCaseWithNecessaryConditions):

    def test_check_if_directory_created_has_params_file_only(self):
        project = Project(self.test_dir)
        project.with_params(params).write()

        tmp_dir = self.list_files()

        self.assertEqual(1, len(tmp_dir))
        self.assertTrue("params.properties" in tmp_dir)

    def test_check_the_content_written_in_params_properties_file(self):
        project = Project(self.test_dir)
        project.with_params(params).write()

        with self.open_file("params.properties") as f:
            expected = "#params.properties\nfailure.emails=email@gmail.com\nretries=2\nretry.backoff=30000\n"
            self.assertEqual(expected, f.read())


class EnvPropertiesFileTest(TestCaseWithNecessaryConditions):

    def test_check_if_directory_created_has_env_file_only(self):
        project = Project(self.test_dir)
        project.with_params(ParamsJoin()(envs)).write()

        tmp_dir = self.list_files()

        self.assertEqual(1, len(tmp_dir))
        self.assertTrue("some_envs.properties" in tmp_dir)

    def test_check_the_content_written_in_envs_properties(self):
        project = Project(self.test_dir)
        project.with_params(ParamsJoin()(envs)).write()

        with self.open_file("some_envs.properties") as f:
            expected = "#some_envs.properties\ncustom.envs="
            content = f.read()
            self.assertTrue(expected in content)
            self.assertTrue("xxxxxxxx" in content)
            self.assertTrue("yarn" in content)


class JobTypeCommandTest(TestCaseWithNecessaryConditions):

    def test_check_if_directory_created_has_job1_command_file_only(self):
        project = Project(self.test_dir, job1_command)
        project.with_params().write()

        tmp_dir = self.list_files()

        self.assertEqual(1, len(tmp_dir))
        self.assertTrue("job1_command.job" in tmp_dir)

    def test_check_the_content_written_in_job1(self):
        project = Project(self.test_dir, job1_command)
        project.with_params().write()

        with self.open_file("job1_command.job") as f:
            expected = "#job1_command.job\ncommand=${python} -c 'from test import test_method; test_method()'\ntype=command\n"
            self.assertEqual(expected, f.read())
