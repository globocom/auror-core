import os

import yaml

from auror_core.v2.job import Job
from auror_core.v2.dumper import Dumper
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
        return self.__as_job_objects(self._jobs)
    
    def __as_job_objects(self, jobs):
        return [self.__build_job(job) for job in jobs]
    
    def __build_job(self, job):
        if job.get('nodes'):
            job['nodes'] = self.__as_job_objects(job.get('nodes'))
        return JobType.get_job_type_class(job.get('type')).build(job)

    def as_python_file(self, directory):
        dumper = Dumper(directory)
        dumper.dump_jobs(*self.as_job_objects())
