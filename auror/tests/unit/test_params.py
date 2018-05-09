#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
from auror.params import Params, Env, SparkExecutor, SparkDriver, ParamsJoin


class ParamsTest(TestCase):

	def setUp(self):
		key_vals = {"name_1": "value_1", "name_2": "value_2"}
		self.data_params = Params("name_teste_params", **key_vals)

	def test_get_itens(self):
		itens_actual = self.data_params._get_items()
		expected = [("name_2", "value_2"), ("name_1", "value_1")]

		self.assertEqual(expected, itens_actual)


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
		self.data_params = Params("custom.env", " ")

