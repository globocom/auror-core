from unittest import TestCase

from auror_core.v2.job import Job, Command


class CommandJobTest(TestCase):

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
    
    def test_build_method_with_one_command(self):
        simple_job = {
            'config': {
                'command': 'COMMAND'
            },
            'dependsOn': ['firstDependencie', 'secondDependecie'],
            'name': 'AZTest',
        }
        actual_job = Command.build(simple_job)

        expected_job = Command(
            simple_job['name'],
            simple_job['config'],
            simple_job['dependsOn']
        ).with_command(simple_job['config']['command'])

        self.assertEqual(expected_job, actual_job)
    
    def test_build_method_with_more_than_one_command(self):
        extra_commands = {
            'command.1': 'COMMAND 2',
            'command.2': 'COMMAND 3',
        }
        job = {
            'config': {
                'command': 'COMMAND'
            },
            'dependsOn': ['firstDependencie', 'secondDependecie'],
            'name': 'AZTest',
        }
        job['config'].update(extra_commands)
        actual_job = Command.build(job)

        expected_job = Command(
            job['name'],
            job['config'],
            job['dependsOn']
        ).with_command(job['config']['command']) \
        .with_another_commands([
            Command._Command(command, command_number.split('.')[-1])
            for command_number, command in extra_commands.items()
        ])

        self.assertEqual(expected_job, actual_job)
