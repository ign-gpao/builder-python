""" Porject's class of the GPAO"""

import json

from gpao.job import Job


def handler(obj):
    """ handler """
    if isinstance(obj, Job):
        dictionary = obj.__dict__.copy()
        noise_keys = ["internal_id"]

        dictionary = {k: v for k,
                      v in dictionary.items() if v and (k not in noise_keys)}

        return dictionary
    return None


class Project:

    """ Project class """

    cpt_id = 0

    def __init__(self, name, jobs=None, deps=None):
        self.name = name
        self.reorganized = False

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

        self.internal_id = Project.cpt_id
        Project.cpt_id += 1

    @staticmethod
    def reset():
        """ Counter reset """
        Project.cpt_id = 0

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

    def reorganize_job_dependencies(self):
        """ Reorganize job's id in deps list """
        for job in self.jobs:
            if job.deps:
                for dep in job.deps:
                    job_id = dep['id']
                    dep['id'] = self.find_job_index(job_id)

        self.reorganized = True

    def find_job_index(self, job_id):
        """ find job's index in project and return this position """
        cpt = 0
        for job in self.jobs:
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

        if not self.reorganized:
            self.reorganize_job_dependencies()

        return json.dumps(dictionary, default=handler, indent=4)

    def is_reorganized(self):
        """ get reorganized var """
        return self.reorganized
