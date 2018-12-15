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

    # called on _add_items for custom types
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
        with open(path, 'w') as writer:
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
