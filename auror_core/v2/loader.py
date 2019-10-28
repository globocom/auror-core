import os
import copy

import yaml

from auror_core.v2.job import Job
from auror_core.v2 import JobType


class Loader:
    def __init__(self, flow_file_path):
        if not os.path.exists(flow_file_path):
            raise ValueError('File does not exists')
        
        self._config, self._jobs = self.__load_yaml(flow_file_path)
    
    def __load_yaml(self, path):
        yaml_file = yaml.safe_load(open(path))
        config = yaml_file['config'] if 'config' in yaml_file.keys() else {}
        return config, yaml_file['nodes']
    
    def as_job_objects(self):
        job_list = []
        for job in self._jobs:
            job = Job() \
                    .as_type(JobType.get_job_type_class(job['type'])) \
                    .with_name(job['name']) \
                    .with_command(job['command']) \
                    .with_another_command(job['anotherCommand'])
            job_list.append(job)
        return job_list

    def as_python_file(self):
        raise NotImplementedError('"as_python_file" method is not implemented yet')
