from auror_core.v2.job import Command


class JobType:
    COMMAND = Command

    @staticmethod
    def get_job_type_class(job_type):
        return getattr(JobType, job_type.upper(), Command)
