import os
from jproperties import Properties

class Params:

    def __init__(self, name="params", **key_vals):
        self.name = name
        self.key_vals = key_vals
        self.properties = Properties()

    def _get_items(self):
        return self.key_vals.items()

    def _add_items(self):
        for name, value in self._get_items():
            self.properties[name] = value

    def _write(self, folder):
        name = "{}.properties".format(self.name)
        path = os.path.join(folder, name)
        with open(path, "wb") as f:
            self.properties.store(f, encoding="utf-8", initial_comments=name, timestamp=False)


class Env(Params):

    def _get_items(self):
        return [("env.{}".format(name), value) for name, value in self.key_vals.items()]


class SparkExecutor(Params):

    def _get_items(self):
        return [(name, "--conf spark.executorEnv.{}={}".format(name, value)) for name, value in self.key_vals.items()]


class SparkDriver(Params):

    def _get_items(self):
        return [(name, "--conf spark.yarn.appMasterEnv.{}={}".format(name, value)) for name, value in self.key_vals.items()]


class ParamsJoin:

    def __init__(self, param_name="custom.envs", separator=" "):
        self.param_name = param_name
        self.separator = separator
        self.properties = Properties()
        self.params_class = []

    def __call__(self, *params_class):
        self.params_class = params_class
        return self

    def _add_items(self):
        param_props = []
        for param_class in self.params_class:
            for name, value in param_class._get_items():
                param_props.append(value)
        self.properties[self.param_name] = self.separator.join(param_props)

    def _write(self, folder):
        name = "{}.properties".format("_".join([param_class.name for param_class in self.params_class]))
        path = os.path.join(folder, name)
        with open(path, "wb") as f:
            self.properties.store(f, encoding="utf-8", initial_comments=name, timestamp=False)
