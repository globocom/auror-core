from unittest import TestCase

from auror_core.v2.job import Job, Command


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
