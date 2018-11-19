import os
import copy
from jproperties import Properties

class Job(object):

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

    # called on _add_items for custom types
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
        if not self.extra.get("command"):
            return self.with_command(command)

        counter = 1
        while self.extra.get("command.{}".format(counter)):
            counter += 1
        return self.with_(**{"command.{}".format(counter): command})


class Flow(Job):
    _type = "flow"
