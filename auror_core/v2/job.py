import os
import copy

import yaml

from collections import namedtuple
from functools import reduce


class Job(object):

    def __init__(self, name="DefaultJob", config=None, dependencies=None, nodes=None, extra=None):
        self.name = name
        self.config = config or {}
        self.dependencies = dependencies or []
        self.nodes = nodes or []
        self.extra = extra or {}
        self.properties = dict(nodes=list())
    
    def __eq__(self, other):
        return (isinstance(other, Job)) and \
            self.name == other.name and \
            self.config == other.config and \
            self.dependencies == other.dependencies and \
            self.nodes == other.nodes and \
            self.extra == other.extra and \
            self.properties == other.properties
    
    def __repr__(self):
        return "{}(name='{}', config={}, dependencies={}, nodes={}, extra={})".format(
            type(self).__name__,
            self.name,
            self.config,
            self.dependencies,
            self.nodes,
            self.extra,
        )

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
        return self.instance(self.name, self.config, self.dependencies, list(nodes), self.extra)

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
    
    @classmethod
    def build(cls, data):
        raise NotImplementedError('"build" method is not implemented')


class Command(Job):
    _type = "command"
    _Command = namedtuple('_Command', ['command', 'command_number'])

    def __eq__(self, other):
        return super(Command, self).__eq__(other) and \
            isinstance(other, Command)
            
    def with_all_default(self):
        return self.instance(self.name, self.config, self.dependencies, self.nodes, self.extra)

    def with_command(self, command):
        return self.with_(command=command)
    
    def with_another_commands(self, commands):
        return reduce(
            lambda instance, command: instance.with_another_command(*command),
            commands,
            self
        )

    def with_another_command(self, command, command_number=None):
        if not command:
            return self
        
        if not self.extra.get("command"):
            return self.with_command(command)
 
        command_number = command_number or self.__get_next_command_number()
        return self.with_(**{"command.{}".format(command_number): command})
    
    def __get_next_command_number(self):
        counter = 1
        while self.extra.get("command.{}".format(counter)):
            counter += 1
        return counter
    
    @classmethod
    def build(cls, data):
        extra_commands = [
            cls._Command(value, key.split('.')[-1])
            for key, value in data['config'].items() if 'command.' in key
        ]
        return cls(
            name=data['name'],
            config=data.get('config'),
            dependencies=data.get('dependsOn'),
            nodes=data.get('nodes'),
            extra=data.get('extra')
        ).with_command(data['config']['command']) \
        .with_another_commands(extra_commands)
