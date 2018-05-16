#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil, tempfile
from unittest import TestCase
from auror import Project
from auror.job import Job, Command, Spark, Python
from auror.params import Params, SparkDriver, ParamsJoin

params = Params(
    "params",
    retries="2",
    **{
        "retry.backoff": "30000",
        "failure.emails": "email@gmail.com"
    }
)

driver_envs = SparkDriver(
    "some_envs",
    SOMETHING_KEY = "xxxxxxxx",
    SPARK_MASTER="yarn"
)

job1_command = Job() \
    .as_type(Command) \
    .with_name("job1_command") \
    .with_command("${python} -c 'from teste import teste_method; teste_method()'")

job2_python = Job() \
    .as_type(Python) \
    .with_name("job2_python") \
    .with_virtualenv("job2_python_virtualenv") \
    .with_command("echo 'Some command to job'") \
    .with_dependencies(job1_command)

job3_spark = Job() \
	.as_type(Spark) \
    .with_name("job3_spark") \
    .with_hadoop_user("hadoop_user") \
    .with_spark_version("1.0.0") \
    .with_dynamic_allocation("2", "5") \
    .with_args("prod yarn") \
    .with_dependencies(job2_python) \
    .with_extra_jars("hdfs:///spark/mysql-connector-java-6.0.6.jar") \
    .with_command("echo 'Hello '") \
    .with_another_command("echo 'World!'")


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

		f = self.open_file("params.properties")
		expected = "#params.properties\nfailure.emails=email@gmail.com\nretries=2\nretry.backoff=30000\n"

		self.assertEqual(expected, f.read())


class EnvPropertiesFileTest(TestCaseWithNecessaryConditions):

	def test_check_if_directory_created_has_env_file_only(self):
		project = Project(self.test_dir)
		project.with_params(ParamsJoin()(driver_envs)).write()

		tmp_dir = self.list_files()

		self.assertEqual(1, len(tmp_dir))
		self.assertTrue("some_envs.properties" in tmp_dir)

	def test_check_the_content_written_in_envs_properties(self):
		project = Project(self.test_dir)
		project.with_params(ParamsJoin()(driver_envs)).write()

		f = self.open_file("some_envs.properties")
		expected = "#some_envs.properties\ncustom.envs=--conf spark.yarn.appMasterEnv.SPARK_MASTER\\=yarn --conf spark.yarn.appMasterEnv.SOMETHING_KEY\\=xxxxxxxx\n"

		self.assertEqual(expected, f.read())


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

		f = self.open_file("job1_command.job")
		expected = "#job1_command.job\ncommand=${python} -c 'from teste import teste_method; teste_method()'\ntype=command\n"

		self.assertEqual(expected, f.read())


class JobTypePythonTest(TestCaseWithNecessaryConditions):

	def test_check_if_directory_created_has_job2_python_file_only(self):
		project = Project(self.test_dir, job2_python)
		project.with_params().write()

		tmp_dir = self.list_files()

		self.assertEqual(1, len(tmp_dir))
		self.assertTrue("job2_python.job" in tmp_dir)

	def test_check_the_content_written_in_job2(self):
		project = Project(self.test_dir, job2_python)
		project.with_params().write()

		f = self.open_file("job2_python.job")
		expected = "#job2_python.job\ncommand=echo 'Some command to job'\ndependencies=job1_command\ntype=python\nvirtualenv=job2_python_virtualenv\n"

		self.assertEqual(expected, f.read())


class JobTypeSparkTest(TestCaseWithNecessaryConditions):

	def test_check_if_directory_created_has_jobs_spark_file_only(self):
		project = Project(self.test_dir, job3_spark)
		project.with_params().write()

		tmp_dir = self.list_files()

		self.assertEqual(1, len(tmp_dir))
		self.assertTrue("job3_spark.job" in tmp_dir)

	def test_check_the_content_written_in_job3(self):
		project = Project(self.test_dir, job3_spark)
		project.with_params().write()

		f = self.open_file("job3_spark.job")
		expected = "#job3_spark.job\nargs=prod yarn\ncommand=${spark.submit.extra.jars}\ncommand.1=echo 'World\\!'"\
				   "\nconf.spark.dynamicAllocation.enabled=true\ndependencies=job2_python\nenv.HADOOP_USER_NAME=hadoop_user\n"\
				   "extra.jars=hdfs\\:///spark/mysql-connector-java-6.0.6.jar\nmax.executors=5\nmin.executors=2\n"\
				   "spark.version=1.0.0\ntype=command\n"

		self.assertEqual(expected, f.read())


class CompleteJobCreationTest(TestCaseWithNecessaryConditions):

	def test_check_if_all_files_were_created_including_parameters_files(self):
		project = Project(self.test_dir, job1_command, job2_python, job3_spark)
		project.with_params(ParamsJoin()(driver_envs), params).write()

		tmp_dir = self.list_files()

		self.assertEqual(5, len(tmp_dir))
		self.assertEqual(project.folder, self.test_dir)
		self.assertTrue("job1_command.job" in tmp_dir)
		self.assertTrue("job2_python.job" in tmp_dir)
		self.assertTrue("job3_spark.job" in tmp_dir)
		self.assertTrue("params.properties" in tmp_dir)
		self.assertTrue("some_envs.properties" in tmp_dir)

	def test_check_if_job2_dependency_is_job1(self):
		project = Project(self.test_dir, job1_command, job2_python, job3_spark)
		project.with_params(ParamsJoin()(driver_envs), params).write()

		f = self.open_file("job2_python.job")

		self.assertTrue("dependencies=job1_command" in f.read())

	def test_check_if_job3_dependency_is_job2(self):
		project = Project(self.test_dir, job1_command, job2_python, job3_spark)
		project.with_params(ParamsJoin()(driver_envs), params).write()

		f = self.open_file("job3_spark.job")

		self.assertTrue("dependencies=job2_python" in f.read())

