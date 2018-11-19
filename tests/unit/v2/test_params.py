#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
import shutil, tempfile
from unittest import TestCase
from auror.v2.params import Params, Env, ParamsJoin


class ParamsTest(TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp() # Create a temporary directory
        key_vals = {"param_name_1": "value_1", "param_name_2": "value_2"}
        self.data_params = Params("name_teste_params", **key_vals)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True) # Remove the directory after the test

    def test_get_items(self):
        itens_actual = self.data_params._get_items()
        expected = [("param_name_2", "value_2"), ("param_name_1", "value_1")]

        self.assertEqual(expected, itens_actual)

    def test_add_items(self):
        self.data_params._add_items()

        self.assertEqual("value_1", self.data_params.properties["config"]["param_name_1"])
        self.assertEqual("value_2", self.data_params.properties["config"]["param_name_2"])

    def test_write_in_folder(self):
        name = "{}.flow".format(path.basename(self.test_dir))
        self.data_params._add_items()
        self.data_params._write(self.test_dir)
        f = open(path.join(self.test_dir, name))
        expected = 'config:\n  param_name_1: value_1\n  param_name_2: value_2\n'

        self.assertEqual(f.read(), expected)


class EnvParamsTest(TestCase):

    def test_get_env_params(self):
        result_actual = Env(TESTE_HADOOP_NAME="hadoop", TESTE_SPARK_MASTER="yarn")._get_items()
        expected = [("env.TESTE_SPARK_MASTER", "yarn"), ("env.TESTE_HADOOP_NAME", "hadoop")]

        self.assertEqual(expected, result_actual)


class ParamsJoinTest(TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.data_params = ParamsJoin("custom.env", " ")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_call_method(self):
        params_class = Env(TESTE_HADOOP_NAME="hadoop", TESTE_SPARK_MASTER="yarn")
        result_actual = self.data_params.__call__(params_class)
        expected = self.data_params.params_class

        self.assertEqual(expected, result_actual.params_class)

    def test_add_items(self):
        params_class = Env(TESTE_HADOOP_NAME="hadoop", TESTE_SPARK_MASTER="yarn")
        result_actual = self.data_params.__call__(params_class)
        result_actual._add_items()
        expected = "yarn hadoop"

        self.assertEqual(expected, result_actual.properties['config']['custom.env'])

    def test_write_in_folder(self):
        params_class = Env(TESTE_HADOOP_NAME="hadoop", TESTE_SPARK_MASTER="yarn")
        result_actual = self.data_params.__call__(params_class)
        name = "{}.flow".format(path.basename(self.test_dir))
        result_actual._add_items()
        result_actual._write(self.test_dir)
        f = open(path.join(self.test_dir, name))
        expected = 'config:\n  custom.env: yarn hadoop\n'

        self.assertEqual(f.read(), expected)

