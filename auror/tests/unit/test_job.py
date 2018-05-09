#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
from auror.job import Job, Command, Spark, Python


class JobTest(TestCase):

	def setUp(self):
		self.data_job = Job("name_teste_job", "dependencies_teste_job", "extra_teste_job")

	def test_get_instances(self):
		instances_job = self.data_job.instance("name_teste_job", "dependencies_teste_job", "extra_teste_job")

		self.assertEqual(instances_job.name, "name_teste_job")
		self.assertEqual(instances_job.dependencies, "dependencies_teste_job")
		self.assertEqual(instances_job.extra, "extra_teste_job")

	def test_as_type(self):
		expected = "python"
		content = self.data_job.as_type(Python)
		actual = content._type

		self.assertEqual(expected, actual)

	def test_with_name(self):
		expected = "teste_name"
		content = self.data_job.with_name("teste_name")
		actual = content.name

		self.assertEqual(expected, actual)

	def test_with_dependencies(self):
		job_1 = self.data_job.with_name("teste_name")
		job_2 = self.data_job.with_dependencies(job_1)
		expected = ["teste_name"]
		actual = job_2.dependencies

		self.assertEqual(expected, actual)


class CommandJobTest(TestCase):

	def test_with_all_default(self): #
		result = Command().with_all_default()
		actual = result.extra
		expected = {}

		self.assertEqual(expected, actual)

	def test_with_command(self):
		command = "${python} -c 'from teste import teste_command_spark; teste_command_spark()'"
		result = Command().with_command(command=command)
		actual = result.extra
		expected = {'command': "${python} -c 'from teste import teste_command_spark; teste_command_spark()'"}

		self.assertEqual('command', result._type)
		self.assertEqual(expected, actual)

	def test_with_another_command_without_a_command(self):
		command = "${python} -c 'from teste import teste_command_spark; teste_command_spark()'"
		result = Command().with_another_command(command=command)
		actual = result.extra
		expected = {'command': "${python} -c 'from teste import teste_command_spark; teste_command_spark()'"}

		self.assertEqual('command', result._type)
		self.assertEqual(expected, actual)

	def test_with_another_command_where_a_command_already_exists(self):
		command_ = "${python} -c 'from teste import teste_command_spark; teste_command_spark()'"
		result_ = Command().with_another_command(command=command_)
		command = "${python} -c 'from teste import teste_command_spark_again; teste_command_spark_again()'"
		result = result_.with_another_command(command=command)
		actual = result.extra
		expected = {'command': "${python} -c 'from teste import teste_command_spark; teste_command_spark()'", 
					'command.1': "${python} -c 'from teste import teste_command_spark_again; teste_command_spark_again()'"}

		self.assertEqual('command', result._type)
		self.assertEqual(expected, actual)


class SparkJobTest(TestCase):

	def test_with_all_default(self):
		result = Spark().with_all_default()
		actual = result.extra
		expected = {'spark.version': '2.2.1', 'driver.memory': '1g', 'queue': 'default',
					'num.executors': '1', 'env.HADOOP_USER_NAME': 'hadoop', 'executor.memory': '1g',
					'executor.cores': '1'}

		self.assertEqual('command', result._type)
		self.assertEqual(expected, actual)

	def test_with_hadoop_user(self):
		result = Spark().with_hadoop_user(hadoop_user='teste')
		actual = result.extra
		expected = {'env.HADOOP_USER_NAME': 'teste'}

		self.assertEqual('command', result._type)
		self.assertEqual(expected, actual)

	def test_with_spark_version(self):
		result = Spark().with_spark_version(spark_version='1.0.0')
		actual = result.extra
		expected = {'spark.version': '1.0.0'}

		self.assertEqual('command', result._type)
		self.assertEqual(expected, actual)

	def test_with_queue(self):
		result = Spark().with_queue(queue='teste')
		actual = result.extra
		expected = {'queue': 'teste'}

		self.assertEqual('command', result._type)
		self.assertEqual(expected, actual)

	def test_driver_memory(self):
		result = Spark().with_driver_memory(driver_memory='1g')
		actual = result.extra
		expected = {'driver.memory': '1g'}

		self.assertEqual('command', result._type)
		self.assertEqual(expected, actual)

	def test_with_executor_memory(self):
		result = Spark().with_executor_memory(executor_memory='1g')
		actual = result.extra
		expected = {'executor.memory': '1g'}

		self.assertEqual('command', result._type)
		self.assertEqual(expected, actual)

	def test_with_executor_cores(self):
		result = Spark().with_executor_cores(executor_cores='1')
		actual = result.extra
		expected = {'executor.cores': '1'}

		self.assertEqual('command', result._type)
		self.assertEqual(expected, actual)

	def test_with_dynamic_allocation(self):
		result = Spark().with_dynamic_allocation(min_executors='1', max_executors='5')
		actual = result.extra
		expected = {"conf.spark.dynamicAllocation.enabled": "true", \
                    "min.executors": '1', "max.executors": '5'}

		self.assertEqual('command', result._type)
		self.assertEqual(expected, actual)

	def test_with_num_executors(self):
		result = Spark().with_num_executors(num_executors='1')
		actual = result.extra
		expected = {'num.executors': '1'}

		self.assertEqual('command', result._type)
		self.assertEqual(expected, actual)

	def test_with_jar_file(self):
		result = Spark().with_jar_file(jar_file='teste/jar/teste-jar-file.jar')
		actual = result.extra
		expected = {'jar.file': 'teste/jar/teste-jar-file.jar'}

		self.assertEqual('command', result._type)
		self.assertEqual(expected, actual)

	def test_with_extra_jars(self):
		result = Spark().with_extra_jars(extra_jars='hdfs\:///spark/teste-jar-1-1.0.0.jar,hdfs\:///spark/teste-jar-2-1.0.0.jar')
		actual = result.extra
		expected = {'extra.jars': 'hdfs\:///spark/teste-jar-1-1.0.0.jar,hdfs\:///spark/teste-jar-2-1.0.0.jar'}

		self.assertEqual('command', result._type)
		self.assertEqual(expected, actual)

	def test_with_java_class(self):
		result = Spark().with_java_class(java_class='com.globo.ab.jobs.teste.SparkJob')
		actual = result.extra
		expected = {'java.class': 'com.globo.ab.jobs.teste.SparkJob'}

		self.assertEqual('command', result._type)
		self.assertEqual(expected, actual)

	def test_with_args(self):
		result = Spark().with_args(some_args='${date} teste-prod teste-yarn')
		actual = result.extra
		expected = {'args': '${date} teste-prod teste-yarn'}

		self.assertEqual('command', result._type)
		self.assertEqual(expected, actual)

	def test_before_add_hook_without_extra_jars(self):
		result = Spark().before_add_hook()
		actual = result.extra
		expected = {'command': '${spark.submit}'}

		self.assertEqual('command', result._type)
		self.assertEqual(expected, actual)

	def test_before_add_hook_with_extra_jars(self):
		result_extra = Spark().with_extra_jars(extra_jars='hdfs\:///spark/teste-jar-1-1.0.0.jar,hdfs\:///spark/teste-jar-2-1.0.0.jar')
		result = result_extra.before_add_hook()
		actual = result.extra
		expected = {'command': '${spark.submit.extra.jars}', 'extra.jars': 'hdfs\\:///spark/teste-jar-1-1.0.0.jar,hdfs\\:///spark/teste-jar-2-1.0.0.jar'}

		self.assertEqual('command', result._type)
		self.assertEqual(expected, actual)


class PythonJobTest(TestCase):

	def test_with_all_default(self):
		result = Python().with_all_default()
		actual = result.extra
		expected = {'python': '${python3}', 'virtualenv.requirements': './requirements.txt'}

		self.assertEqual('python', result._type)
		self.assertEqual(expected, actual)

	def test_with_python(self):
		result = Python().with_python(python='${python}')
		actual = result.extra
		expected = {'python': '${python}'}

		self.assertEqual('python', result._type)
		self.assertEqual(expected, actual)

	def test_with_virtualenv(self):
		result = Python().with_virtualenv(virtualenv='teste')
		actual = result.extra
		expected = {'virtualenv': 'teste'}

		self.assertEqual('python', result._type)
		self.assertEqual(expected, actual)

	def test_with_requirements(self):
		result = Python().with_requirements(requirements="./teste.txt")
		actual = result.extra
		expected = {'virtualenv.requirements': './teste.txt'}

		self.assertEqual('python', result._type)
		self.assertEqual(expected, actual)

