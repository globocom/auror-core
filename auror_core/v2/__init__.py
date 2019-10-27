from auror_core.v2.job import Command


class JobType:
    COMMAND = Command

    @staticmethod
    def get_job_type_class(job_type):
        _job_type = getattr(JobType, job_type.upper(), None)
        if not _job_type:
            raise ValueError('Invalid job type: {}'.format(job_type))
        return _job_type
