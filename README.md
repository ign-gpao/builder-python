# IGN GPAO Project Builder

IGN GPAO Project Builder est une bibliothèque python de création de projet au format JSON pour la [GPAO](https://github.com/ign-gpao).

## Prérequis

 - Python 3 ou plus

## Installation

Vous pouvez la télécharger depuis les dépôts officiels de [PyPI](https://pypi.org/project/ign-gpao-project-builder/):

    pip install ign-gpao-project-builder

## Exemple d'utilisation

``` python
from gpao.builder import Builder
from gpao.project import Project
from gpao.job import Job

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


job8 = Job("job8", "touch file")
job8bis = Job("job8bis", "touch file", job8)
project4 = Project("project4",  [job8, job8bis])

job9 = Job("job9", "touch file")
project5 = Project("project5",  [job9], [project4])

builder = Builder([project4, project5])

builder.send_project_to_api("http://localhost:8080")
```
  
Cet exemple sauvegarde un fichier `project.json` avec le contenu suivant :

```
{
    "projects": [
        {
            "name": "project1",
            "jobs": [
                {
                    "name": "job1",
                    "command": "touch file",
                    "tags": [
                        "tag1",
                        "tag2"
                    ]
                },
                {
                    "name": "job2",
                    "command": "touch file"
                },
                {
                    "name": "job3",
                    "command": "touch file",
                    "deps": [
                        {
                            "id": 0
                        },
                        {
                            "id": 1
                        }
                    ],
                    "tags": [
                        "tag1",
                        "tag2"
                    ]
                }
            ]
        },
        {
            "name": "project2",
            "jobs": [
                {
                    "name": "job4",
                    "command": "touch file"
                },
                {
                    "name": "job5",
                    "command": "touch file",
                    "deps": [
                        {
                            "id": 0
                        }
                    ]
                }
            ]
        },
        {
            "name": "project3",
            "jobs": [
                {
                    "name": "job6",
                    "command": "touch file"
                },
                {
                    "name": "job7",
                    "command": "touch file",
                    "deps": [
                        {
                            "id": 0
                        }
                    ]
                }
            ],
            "deps": [
                {
                    "id": 0
                },
                {
                    "id": 1
                }
            ]
        }
    ]
}
```

### Création de jobs avec attribut geometry

On peut définir une géométrie pour chaque job avec l'attribut geometry. Dans la base de données elle est définie en WGS84 (epsg:4326).

Cette geometrie peut-être renseignée en :
* binaire, exemple :
``` python
geom1 = "0106000020E61000000100000001030000000100000005000000500834AD72D51540CB389A27B9084740C28E5BF782D715401DA21CCD7B0E474072E2A118C5191640D6667F3B4D0E4740D9D3A6EEA6171640108BB99F8A084740500834AD72D51540CB389A27B9084740"
job_with_geom1 = Job("job_with_geom", "sleep 5", geometry=geom1)
```
* texte, exemples :
``` python 
geom2 = 'SRID=2154;POINT(736000 6917000)'
job_with_geom2 = Job("job_with_geom", "sleep 5", geometry=geom2)

geom3 = "SRID=2154;POLYGON((736000 6917000 , 737000 6917000 , 737000 6918000 , 736000 6918000 , 736000 6917000))"
job_with_geom3 = Job("job_with_geom", "sleep 5", geometry=geom3)

```

Elle peut aussi être définie à postériori avec une liste de coordonnées et le SRID, exemple :
* pour un point
``` python
job_with_geom4 = Job("job_with_geom", "sleep 5")
job_with_geom4.add_geometry_from_coordinates('2154', [(736000, 6917000)])

```
* pour un polygone (triangle = 3 coords, carré = 4 coords, etc)
``` python
job_with_geom5 = Job("job_with_geom", "sleep 5")
job_with_geom5.add_geometry_from_coordinates('2154', [(736000, 6917000) , (737000, 6917000) , (737000, 6918000) , (736000, 6918000)])
```

Ci-dessous, un exemple de fonction qui ajoute une geometrie à partir du nom des jobs suivants la règle d'appellation "Name_AAAA_XXXX_YYYYY_LA93_IGN69" :
``` python
def add_geometry_from_job_name(job):
    job_name = job.name
    job_name = job_name.split('_')
    SRID = 4326
    if job_name[4]=='LA93':
        SRID = 2154
    coords = [(job_name[2]+"000", job_name[3]+"000")]
    job.add_geometry_from_coordinates(SRID, coords)

job_with_geom6 = Job("Semis_2023_0736_6917_LA93_IGN69", "sleep 5")
add_geometry_from_job_name(job_with_geom6)
```

### Licence

Ce projet est sous licence CECILL-B (voir [LICENSE.md](https://github.com/ign-gpao/.github/blob/main/LICENSE.md)).

[![IGN](https://github.com/ign-gpao/.github/blob/main/images/logo_ign.png)](https://www.ign.fr)
