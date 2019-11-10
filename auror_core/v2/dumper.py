import os

import autopep8


class Dumper:
    
    DEFAULT_IMPORTS = 'from auror_core.v2.job import Command\n\n\n'

    def __init__(self, path):
        if not os.path.exists(path):
            raise ValueError('Directory, {}, does not exist'.format(path))
        self.path = path

    def dump_jobs(self, *jobs):
        _path = '{}/flow.py'.format(self.path)
        with open(_path, 'w') as _file:
            _file.write(self.DEFAULT_IMPORTS)
            for job_number, job in enumerate(jobs):
                _file.write('job_{} = {}\n\n'.format(job_number, repr(job)))
        self.__format_file(_path)

    def __format_file(self, path):
        autopep8.fix_file(
            path,
            options=autopep8.parse_args(
                ['--in-place', '--aggressive', path]
            )
        )
