import copy
from jproperties import Properties

class Project:
    def __init__(self, folder, *jobtypes):
        self.jobtypes = jobtypes
        self.folder = folder
        self.properties = Properties()
        self.params = []
    
    def write(self):

        for jobtype in self.jobtypes:
            jobtype._add_items()
            jobtype._write(self.folder)

        for param in self.params:
            param._add_items()
            param._write(self.folder)
    

    def with_params(self, *paramtypes):
        
        self.params = paramtypes

        return copy.deepcopy(self)