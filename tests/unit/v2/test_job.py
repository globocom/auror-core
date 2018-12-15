#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
import shutil, tempfile
from unittest import TestCase
from auror_core.v2.job import Job, Command


class JobTest(TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp() # Create a temporary directory
        self.data_job = Job("test_job_name", None, ["other_job_name"], None,
                           {"executor.cores": "2", "driver.memory": "6g"})

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True) # Remove the directory after the test

    def test_get_instances(self):
        instance_job = self.data_job.instance("test_job_name_x", None, ["other_job_name_x"], None, {"executor.cores": "2"})

        self.assertIsInstance(instance_job, Job)

    def test_as_type(self):
        expected = "command"
        content = self.data_job.as_type(Command)
        actual = content._type

        self.assertEqual(expected, actual)

    def test_with_name(self):
        expected = "test_job_name_x"
        content = self.data_job.with_name("test_job_name_x")
        actual = content.name

        self.assertEqual(expected, actual)

    def test_with_dependencies(self):
        data_job = Job("test_job_name_2", ["test_job_name_2"], {"driver.memory": "5g"})
        content = self.data_job.with_dependencies(data_job)
        expected = ["test_job_name_2"]
        actual = content.dependencies

        self.assertEqual(expected, actual)

    def test_with_method(self):
        extra = {"env.HADOOP_USER_NAME": "hadoop", "spark.version": "1.0.0"}
        content = self.data_job.with_(**extra)
        expected = {"executor.cores": "2", "driver.memory": "6g", "env.HADOOP_USER_NAME": "hadoop", "spark.version": "1.0.0"}
        actual = content.extra

        self.assertEqual(expected, actual)

    def test_write_in_folder(self):
        content = self.data_job.as_type(Command)
        content._add_items()
        content._write(self.test_dir)
        with open(path.join(self.test_dir, path.basename(self.test_dir)+".flow")) as f:
            expected = "nodes:\n- config:\n    driver.memory: 6g\n    executor.cores: '2'\n  dependsOn:\n  - other_job_name\n  name: test_job_name\n  nodes: []\n  type: command\n"
            self.assertEqual(f.read(), expected)

    def test_add_items_and_it_contains_one_dependency(self):
        content = self.data_job.as_type(Command)
        content._add_items()

        self.assertEqual("other_job_name", content.properties["nodes"][0]["dependsOn"][0])
        self.assertEqual("command", content.properties["nodes"][0]["type"])
        self.assertEqual("2", content.properties["nodes"][0]["config"]["executor.cores"])
        self.assertEqual("6g", content.properties["nodes"][0]["config"]["driver.memory"])

    def test_add_items_and_it_contains_two_dependencies(self):
        data_job = Job("test_job_name", [], {})
        data_job_2 = Job("test_job_name_2", [], {})
        content = self.data_job.with_dependencies(data_job, data_job_2).as_type(Command)
        content._add_items()

        self.assertEqual(["test_job_name", "test_job_name_2"], content.properties["nodes"][0]["dependsOn"])
        self.assertEqual("command", content.properties["nodes"][0]["type"])
        self.assertEqual("2", content.properties["nodes"][0]["config"]["executor.cores"])
        self.assertEqual("6g", content.properties["nodes"][0]["config"]["driver.memory"])

    def test_add_items_and_it_does_not_contain_dependencies(self):
        data_job_x = Job("name_teste_job_4", None, [], None, {"spark.version": "1.0.1"})
        content = data_job_x.as_type(Command)
        content._add_items()

        self.assertEqual(None, content.properties["nodes"][0].get("dependsOn"))
        self.assertEqual("command", content.properties["nodes"][0]["type"])


class CommandJobTest(TestCase):

    def test_with_all_default(self):
        expected = Job("test_job_name", None, ["other_job_name"], None,
                            {"executor.cores": "2", "driver.memory": "6g"})

        self.assertIsInstance(expected, Job)

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