import copy

class Project(object):

    def __init__(self, folder, *jobtypes):
        self.jobtypes = jobtypes
        self.folder = folder
        self.params = []
        self.version = 1

    def is_v2(self):
        self.version = 2
        return copy.deepcopy(self)

    def is_v1(self):
        self.version = 1
        return copy.deepcopy(self)

    def with_params(self, *paramtypes):
        self.params = paramtypes
        return copy.deepcopy(self)

    def write(self):
        for jobtype in self.jobtypes:
            jobtype._add_items()
            jobtype._write(self.folder)

        for param in self.params:
            param._add_items()
            param._write(self.folder)