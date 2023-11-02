""" Reader's class of the gpao """
import json
import requests

class Reader:
    """ Reader of GPAO's monitor """

    def __init__(self):
        pass
        
    def get_projects(self, base_url_api):
        response = requests.get(f"{base_url_api}/api/projects")
        return json.loads(response.text)

    def get_jobs(self, base_url_api):
        response = requests.get(f"{base_url_api}/api/jobs")
        return json.loads(response.text)

    def get_jobs(self, base_url_api):
        response = requests.get(f"{base_url_api}/api/jobs")
        return json.loads(response.text)

    def get_sessions(self, base_url_api):
        response = requests.get(f"{base_url_api}/api/sessions")
        return json.loads(response.text)

    def get_nodes(self, base_url_api):
        response = requests.get(f"{base_url_api}/api/nodes")
        return json.loads(response.text)
