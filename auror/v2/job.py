import os
import copy
import yaml

class Job(object):

    def __init__(self, name="DefaultJob", config=None, dependencies=None, nodes=None, extra=None):
        self.name = name
        self.config = config or {}
        self.dependencies = dependencies or []
        self.nodes = nodes or []
        self.extra = extra or {}
        self.properties = dict(nodes=list())

    def instance(self, name, config, dependencies, nodes, extra):
        return self.__class__(name, config, dependencies, nodes, extra)

    def as_type(self, type_class):
        return type_class(self.name, self.config, self.dependencies, self.nodes, self.extra)

    def with_name(self, name):
        return self.instance(name, self.config, self.dependencies, self.nodes, self.extra)
    
    def with_config(self, config):
        return self.instance(name, self.config, self.dependencies, self.nodes, self.extra)

    def with_dependencies(self, *dependencies):
        dependencies = [dependency.name for dependency in dependencies]
        return self.instance(self.name, self.config, dependencies, self.nodes, self.extra)

    def with_nodes(self, *nodes):
        return self.instance(self.name, self.config, self.dependencies, nodes, self.extra)

    def with_(self, **extra):
        self_extra = copy.deepcopy(self.extra)
        self_extra.update(extra)
        return self.instance(self.name, self.config, self.dependencies, self.nodes, self_extra)

    # chamado no _add_items por aqueles que tem type diferente de 'command'
    def before_add_hook(self):
        return self.instance(self.name, self.config, self.dependencies, self.nodes, self.extra)

    def _write(self, folder):
        name = os.path.basename(folder)
        path = "{}.flow".format(os.path.join(folder, name))
        try:
            with open(path, 'rb') as reader:
                data = yaml.load(reader)
            data.update(self.properties)
        except IOError:
            data = self.properties
        with open(path, 'wb') as writer:
            writer.write(
                yaml.dump(data, default_flow_style=False)
            )
    
    def _get_subnodes(self, job):
        return [node.properties["nodes"] for node in job.nodes]

    def _get_node(self, job):
        node_dict = dict()
        node_dict["name"] = job.name
        node_dict["type"] = job._type
        node_dict["config"] = job.config
        node_dict["nodes"] = self._get_subnodes(job)
        for name, value in job.extra.items():
            node_dict["config"][name] = value
        if job.dependencies:
            node_dict["dependsOn"] = job.dependencies
        return node_dict

    def _add_items(self):
        job = self.before_add_hook()
        self.properties["nodes"].append(self._get_node(job))



class Command(Job):
    _type = "command"

    def with_all_default(self):
        return self.instance(self.name, self.config, self.dependencies, self.nodes, self.extra)

    def with_command(self, command):
        return self.with_(command=command)

    def with_another_command(self, command):
        if not self.extra.get("command"):
            return self.with_command(command)

        counter = 1
        while self.extra.get("command.{}".format(counter)):
            counter += 1
        return self.with_(**{"command.{}".format(counter): command})


class Spark(Command):

    def with_all_default(self):
        return self.with_hadoop_user()\
            .with_spark_version()\
            .with_queue()\
            .with_driver_memory()\
            .with_executor_memory()\
            .with_executor_cores()\
            .with_num_executors()\

    def with_hadoop_user(self, hadoop_user="hadoop"):
        return self.with_(**{"env.HADOOP_USER_NAME":hadoop_user})

    def with_spark_version(self, spark_version="2.2.1"):
        return self.with_(**{"spark.version":spark_version})

    def with_queue(self, queue="default"):
        return self.with_(queue=queue)

    def with_driver_memory(self, driver_memory="1g"):
        return self.with_(**{"driver.memory":driver_memory})

    def with_executor_memory(self, executor_memory="1g"):
        return self.with_(**{"executor.memory":executor_memory})

    def with_executor_cores(self, executor_cores="1"):
        return self.with_(**{"executor.cores":executor_cores})

    def with_dynamic_allocation(self, min_executors="1", max_executors="1"):
        set_configs = {"conf.spark.dynamicAllocation.enabled": "true", \
                       "min.executors": min_executors, "max.executors": max_executors}
        return self.with_(**set_configs)
        
    def with_num_executors(self, num_executors="1"):
        return self.with_(**{"num.executors":num_executors})

    def with_jar_file(self, jar_file):
        return self.with_(**{"jar.file":jar_file})

    def with_extra_jars(self, extra_jars):
        return self.with_(**{"extra.jars":extra_jars})

    def with_java_class(self, java_class):
        return self.with_(**{"java.class":java_class})

    def with_args(self, some_args):
        return self.with_(**{"args":some_args})

    def before_add_hook(self):
        if "extra.jars" in self.extra:
            return self.with_command("${spark.submit.extra.jars}")
        else:
            return self.with_command("${spark.submit}")


class Python(Command):
    _type = "python"

    def with_all_default(self):
        return self.with_python()\
            .with_requirements()

    def with_python(self, python="${python3}"):
        return self.with_(python=python)

    def with_virtualenv(self, virtualenv):
        return self.with_(virtualenv=virtualenv)

    def with_requirements(self, requirements="./requirements.txt"):
        return self.with_(**{"virtualenv.requirements":requirements})


class Email(Job):
    _type = "email"

    def with_subject(self, mail_subject):
        return self.with_(**{"mail.subject": mail_subject})

    def with_message(self, mail_message):
        return self.with_(**{"mail.message": mail_message})

    def with_to_recipient(self, mail_to):
        return self.with_(**{"mail.to": mail_to})

    def message_with_broken_lines(self, mail_message):
        counter = 1
        while self.extra.get("mail.message.{}".format(counter)):
            counter += 1
        return self.with_(**{"mail.message.{}".format(counter): mail_message})

    def with_send(self, mail_send="true"):
        return self.with_(**{"mail.send": mail_send})
