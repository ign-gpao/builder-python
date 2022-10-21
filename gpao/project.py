""" Porject's class of the GPAO"""

import json

from gpao.job import Job


def handler(obj):
    """ handler """
    if isinstance(obj, Job):
        dictionary = obj.__dict__.copy()
        del dictionary["internal_id"]

        dictionary = {k: v for k, v in dictionary.items() if v}
        return dictionary
    return None


class Project:

    """ Project class """

    _cpt_id = 0

    def __init__(self, name, jobs=None, deps=None):
        self.name = name

        self.jobs = []

        if jobs is not None:
            self.jobs.extend(jobs)

        self.deps = []
        if deps is not None:
            if isinstance(deps, Project):
                self.deps.append({"id": deps.get_internal_id()})
            elif isinstance(deps, list):
                for project in deps:
                    self.deps.append({"id": project.get_internal_id()})

        self.internal_id = Project._cpt_id
        Project._cpt_id += 1

    @staticmethod
    def reset():
        """ Counter reset """
        Project._cpt_id = 0

    def get_internal_id(self):
        """ Get internal id """
        return self.internal_id

    def add_dependency(self, dep):
        """ Add a dependencie to this job"""
        if isinstance(dep, Project):
            self.deps.append({"id": dep.get_internal_id()})
        else:
            self.deps.append(dep)

    def add_job(self, job):
        """ Add job into project """
        self.jobs.append(job)

    def get_name(self):
        """ Get name of the project """
        return self.name

    @staticmethod
    def reorganize_job_dependencies(project):
        """ Reorganize job's id in deps list """
        for job in project.jobs:
            if job.deps:
                for dep in job.deps:
                    job_id = dep['id']
                    dep['id'] = Project.find_job_index(project, job_id)

    @staticmethod
    def find_job_index(project, job_id):
        """ find job's index in project and return this position """
        cpt = 0
        for job in project.jobs:
            if job.get_internal_id() == job_id:
                return cpt
            cpt += 1

        return -1

    def to_json(self):
        """ Convert to json """
        # del internal id from project
        dictionary = self.__dict__.copy()
        del dictionary["internal_id"]

        dictionary = {k: v for k, v in dictionary.items() if v}

        Project.reorganize_job_dependencies(self)

        return json.dumps(dictionary, default=handler, indent=4)
