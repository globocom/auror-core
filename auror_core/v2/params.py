import os
import yaml

class Params(object):

    def __init__(self, name="params", **key_vals):
        self.name = name
        self.key_vals = key_vals
        self.properties = dict(config=dict())

    def _get_items(self):
        return list(self.key_vals.items())

    def _add_items(self):
        self.properties['config'] = dict(self._get_items())

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

class Env(Params):

    def _get_items(self):
        return [("env.{}".format(name), value) for name, value in self.key_vals.items()]



class ParamsJoin(Params):

    def __init__(self, param_name="custom.envs", separator=" "):
        self.param_name = param_name
        self.separator = separator
        self.properties = dict(config=dict())
        self.params_class = []

    def __call__(self, *params_class):
        self.params_class = params_class
        return self

    def _add_items(self):
        param_props = []
        for param_class in self.params_class:
            for name, value in param_class._get_items():
                param_props.append(value)
        self.properties["config"][self.param_name] = self.separator.join(param_props)