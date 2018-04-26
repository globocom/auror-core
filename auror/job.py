import os
import copy
from jproperties import Properties

class Job:

    def __init__(self, name="DefaultJob", dependencies=None, extra=None):
        self.name = name
        self.dependencies = dependencies or []
        self.extra = extra or {}
        self.properties = Properties()

    def instance(self, name, dependencies, extra):
        return self.__class__(name, dependencies, extra)

    def as_type(self, type_class):
        return type_class(self.name, self.dependencies, self.extra)

    def with_name(self, name):
        return self.instance(name, self.dependencies, self.extra)

    def with_dependencies(self, *dependencies):
        dependencies = [dependency.name for dependency in dependencies]
        return self.instance(self.name, dependencies, self.extra)

    def with_(self, **extra):
        self_extra = copy.deepcopy(self.extra)
        self_extra.update(extra)
        return self.instance(self.name, self.dependencies, self_extra)

    # chamado no _add_items por aqueles que tem type diferente de 'command'
    def before_add_hook(self):
        return self.instance(self.name, self.dependencies, self.extra)

    def _write(self, folder):
        name = "{}.job".format(self.name)
        path = os.path.join(folder, name)
        with open(path, "wb") as f:
            self.properties.store(f, encoding="utf-8", initial_comments=name, timestamp=False)
    
    def _add_items(self):
        job = self.before_add_hook()
        self.properties["type"] = job._type
        for name, value in job.extra.items():
            self.properties[name] = value
        if self.dependencies:
            self.properties["dependencies"] = ",".join(job.dependencies)


class Command(Job):
    _type = "command"

    def with_all_default(self):
        return self.instance(self.name, self.dependencies, self.extra)

    def with_command(self, command):
        return self.with_(command=command)

    def with_another_command(self, command):
        if not self.get("command"):
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
            .with_min_executors()\
            .with_max_executors()

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

    def with_num_executors(self, num_executors="1"):
        return self.with_(**{"num.executors":num_executors})

    def with_min_executors(self, min_executors="1"):
        return self.with_(**{"min.executors":min_executors})

    def with_max_executors(self, max_executors="1"):
        return self.with_(**{"max.executors":max_executors})

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


class Flow(Job):
    _type = "flow"
