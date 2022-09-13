""" Job's class of the gpao """

import json


class Job:
    """ Job's Class """

    cpt_id = 0

    def __init__(self, name, command, deps=None, tags=None):
        """ constructor"""

        self.name = name
        self.command = command

        self.deps = []

        if deps is not None:
            if isinstance(deps, Job):
                self.deps.append({"id": deps.get_internal_id()})
            elif isinstance(deps, list):
                for job in deps:
                    self.deps.append({"id": job.get_internal_id()})

        self.tags = []
        if tags is not None:
            self.tags.extend(tags)

        self.internal_id = Job.cpt_id
        Job.cpt_id += 1

    def get_internal_id(self):
        """ Get internal id """
        return self.internal_id

    def add_dependency(self, dep):
        """ Add a dependencie to this job"""
        if isinstance(dep, Job):
            self.deps.append({"id": dep.get_internal_id()})
        else:
            self.deps.append(dep)

    def to_json(self):
        """ convert to json string"""
        # del internal id from job
        dictionary = self.__dict__.copy()
        del dictionary["internal_id"]

        dictionary = {k: v for k, v in dictionary.items() if v}

        return json.dumps(dictionary, indent=4)
