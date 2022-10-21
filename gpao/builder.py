""" Builder's class of the gpao """

import json
from gpao.project import Project


def handler(obj):
    """ handler"""
    dictionary = obj.__dict__.copy()
    del dictionary["internal_id"]

    # Remove empty key (deps, tags) and store in a new dictionary tmp
    dictionary = {k: v for k, v in dictionary.items() if v}

    return dictionary


class Builder:
    """ Builder of GPAO's json project """

    def __init__(self, projects=None):
        """constructeur"""

        self.projects = []

        if projects is not None:
            self.projects.extend(projects)

    def add_project(self, project):
        """ Add project """
        self.projects.append(project)

    def save_as_json(self, file_json):
        """ Write Json File """

        json_gpao = {"projects": []}
        for project in self.projects:
            Project.reorganize_job_dependencies(project)
            json_gpao["projects"].append(project)
        with open(file_json, "w", encoding="utf-8") as fjson:
            json.dump(
                json_gpao,
                fjson,
                default=handler,
                ensure_ascii=False,
                indent=4
                )
        Project.reset()
