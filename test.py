""" script test """
import json

from gpao.builder import Builder
from gpao.project import Project
from gpao.job import Job


def is_valid(json1, json2):
    """ Fonction test """

    with open(json1, encoding="utf-8") as file:
        data1 = json.load(file)

    with open(json2, encoding="utf-8") as file:
        data2 = json.load(file)

    if data1 == data2:
        return True

    return False


job1 = Job("job1", "touch file", tags=["tag1", "tag2"])
job2 = Job("job2", "touch file")
job3 = Job("job3", "touch file", job1, tags=["tag1", "tag2"])
job3.add_dependency(job2)

# print(job1.to_json())
# print(job2.to_json())
# print(job3.to_json())

project1 = Project("project1", [job1, job2, job3])
# print(project1.to_json())

job4 = Job("job4", "touch file")
job5 = Job("job5", "touch file")
job5.add_dependency(job4)

project2 = Project("project2", [job4, job5])

# print(project2.to_json())

job6 = Job("job6", "touch file")
job7 = Job("job7", "touch file", job6)
project3 = Project("project3", [job6, job7], [project1, project2])

# print(project3.to_json())

builder = Builder([project1, project2])
builder.add_project(project3)

builder.save_as_json("project.json")
builder.save_as_json("project_bis.json")

if is_valid("project.json", "project_bis.json"):
    print("sending to API")
    builder.send_project_to_api("http://localhost:8080")
else:
    print("Error, not same json")


job8 = Job("job8", "touch file")
job8bis = Job("job8bis", "touch file", job8)
project4 = Project("project4",  [job8, job8bis])

job9 = Job("job9", "touch file")
project5 = Project("project5",  [job9], [project4])

builder = Builder([project4, project5])

builder.save_as_json("project2.json")
builder.save_as_json("project2_bis.json")

if is_valid("project2.json", "project2_bis.json"):
    print("sending to API")
    builder.send_project_to_api("http://localhost:8080")
else:
    print("Error, not same json")
