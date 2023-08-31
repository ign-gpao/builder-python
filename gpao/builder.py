""" Builder's class of the gpao """

import json
import requests
from gpao.project import Project
from gpao.job import Job


def handler(obj):
    """ handler"""
    dictionary = obj.__dict__

    noise_keys = ["internal_id", "reorganized"]

    dictionary = {k: v for k,
                  v in dictionary.items() if v and (k not in noise_keys)}

    return dictionary


class Builder:
    """ Builder of GPAO's json project """

    def __init__(self, projects=None):
        """constructeur"""

        self.projects = []
        # Project.reset()
        # Job.reset()

        if projects is not None:
            self.projects.extend(projects)

    def add_project(self, project):
        """ Add project """
        self.projects.append(project)

    def save_as_json(self, file_json):
        """ Write Json File """

        json_gpao = {"projects": []}
        for project in self.projects:
            if not project.is_reorganized():
                project.reorganize_job_dependencies()
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
        Job.reset()

    def send_project_to_api(self, base_url_api):
        """ Send To API """
        json_gpao = {"projects": []}
        for project in self.projects:
            if not project.is_reorganized():
                project.reorganize_job_dependencies()
            json_gpao["projects"].append(project)

        json_str = json.dumps(
                json_gpao,
                default=handler,
                ensure_ascii=False,
                indent=4
                )

        url = base_url_api+"/api/project"
        try:
            headers = {
                "Content-type": "application/json",
            }

            req = requests.put(url, data=json_str, headers=headers, timeout=60)
            req.raise_for_status()
        except requests.exceptions.RequestException as exception:
            print("Impossible d'envoyer la requête API sur",
                  url, ": ERROR => ",
                  exception)

        Project.reset()
        Job.reset()
