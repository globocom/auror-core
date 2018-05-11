#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
from auror.params import Params, Env, SparkExecutor, SparkDriver, ParamsJoin


class ParamsTest(TestCase):

	def setUp(self):
		key_vals = {"name_1": "value_1", "name_2": "value_2"}
		self.data_params = Params("name_teste_params", **key_vals)

	def test_get_items(self):
		itens_actual = self.data_params._get_items()
		expected = [("name_2", "value_2"), ("name_1", "value_1")]

		self.assertEqual(expected, itens_actual)

	def test_add_items(self):
		self.data_params._add_items()

		self.assertEqual("value_1", self.data_params.properties["name_1"][0])
		self.assertEqual("value_2", self.data_params.properties["name_2"][0])


class EnvParamsTest(TestCase):

	def test_get_env_params(self):
		result_actual = Env(TESTE_HADOOP_NAME="hadoop", TESTE_SPARK_MASTER="yarn")._get_items()
		expected = [("env.TESTE_SPARK_MASTER", "yarn"), ("env.TESTE_HADOOP_NAME", "hadoop")]

		self.assertEqual(expected, result_actual)


class SparkExecutorParamsTest(TestCase):

	def test_get_spark_executor_params(self):
		result_actual = SparkExecutor(TESTE_HADOOP_NAME="hadoop", TESTE_SPARK_MASTER="yarn")._get_items()
		expected = [("TESTE_SPARK_MASTER", "--conf spark.executorEnv.TESTE_SPARK_MASTER=yarn"),
					("TESTE_HADOOP_NAME", "--conf spark.executorEnv.TESTE_HADOOP_NAME=hadoop")]

		self.assertEqual(expected, result_actual)


class SparkDriverParamsTest(TestCase):

	def test_get_spark_driver_params(self):
		result_actual = SparkDriver(TESTE_HADOOP_NAME="hadoop", TESTE_SPARK_MASTER="yarn")._get_items()
		expected = [("TESTE_SPARK_MASTER", "--conf spark.yarn.appMasterEnv.TESTE_SPARK_MASTER=yarn"),
					("TESTE_HADOOP_NAME", "--conf spark.yarn.appMasterEnv.TESTE_HADOOP_NAME=hadoop")]

		self.assertEqual(expected, result_actual)


class ParamsJoinTest(TestCase):

	def setUp(self):
		self.data_params = ParamsJoin("custom.env", " ")

	def test_call_method(self):
		params_class = SparkDriver(TESTE_HADOOP_NAME="hadoop", TESTE_SPARK_MASTER="yarn")
		result_actual = self.data_params.__call__(params_class)
		expected = self.data_params.params_class

		self.assertEqual(expected, result_actual.params_class)

	def test_add_items(self):
		params_class = SparkDriver(TESTE_HADOOP_NAME="hadoop", TESTE_SPARK_MASTER="yarn")
		result_actual = self.data_params.__call__(params_class)
		result_actual._add_items()
		expected = "--conf spark.yarn.appMasterEnv.TESTE_SPARK_MASTER=yarn --conf spark.yarn.appMasterEnv.TESTE_HADOOP_NAME=hadoop"

		self.assertEqual(expected, result_actual.properties[result_actual.param_name][0])

