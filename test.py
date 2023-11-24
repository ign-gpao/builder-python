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


# Exemple de jobs avec geometry

# Les différentes manières de renseigner l'attribut geometry :

# en binaire
geom1 = "0106000020E61000000100000001030000000100000005000000500834AD72D51540C"
+"B389A27B9084740C28E5BF782D715401DA21CCD7B0E474072E2A118C5191640D6667F3B4D0E4"
+"740D9D3A6EEA6171640108BB99F8A084740500834AD72D51540CB389A27B9084740"
job_with_geom1 = Job("job_with_geom", "sleep 5", geometry=geom1)

# en texte
geom2 = 'SRID=2154;POINT(736000 6917000)'
job_with_geom2 = Job("job_with_geom", "sleep 5", geometry=geom2)

geom3 = "SRID=2154;POLYGON((736000 6917000 , 737000 6917000 , 737000 6918000 "
+", 736000 6918000 , 736000 6917000))"
job_with_geom3 = Job("job_with_geom", "sleep 5", geometry=geom3)

# À postériori avec une liste de coordonnées et le SRID

# pour un point
job_with_geom4 = Job("job_with_geom", "sleep 5")
job_with_geom4.add_geometry_from_coordinates('2154', [(736000, 6917000)])

# pour un polygone (carré = 4 points)
job_with_geom5 = Job("job_with_geom", "sleep 5")
job_with_geom5.add_geometry_from_coordinates('2154',
                                             [(736000, 6917000),
                                              (737000, 6917000),
                                              (737000, 6918000),
                                              (736000, 6918000)])

# A partir d'une fonction que chacun prendra le soin d'écrire selon leurs
# regles d'appellation des jobs, exemple :


def add_geometry_from_job_name(job):
    job_name = job.name
    job_name = job_name.split('_')
    SRID = 4326
    if job_name[4] == 'LA93':
        SRID = 2154
    coords = [(job_name[2]+"000", job_name[3]+"000")]
    job.add_geometry_from_coordinates(SRID, coords)


job_with_geom6 = Job("Semis_2023_0736_6917_LA93_IGN69", "sleep 5")
add_geometry_from_job_name(job_with_geom6)


project_map1 = Project("project-map1",  [job_with_geom1,
                                         job_with_geom2,
                                         job_with_geom3])
project_map2 = Project("project-map2",  [job_with_geom4, job_with_geom5])
project_map3 = Project("project-map3",  [job_with_geom6])

builder = Builder([project_map1, project_map2, project_map3])

builder.save_as_json("project-map.json")

builder.send_project_to_api("http://localhost:8080")
