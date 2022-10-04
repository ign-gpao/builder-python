# IGN GPAO Project Builder

IGN GPAO Project builder est une bibliothèque python de création de projet au format JSON pour la [GPAO](https://github.com/ign-gpao).

## Prérequis

 - Python 3 ou plus

## Installation

Vous pouvez la télécharger depuis les dépôts officiels de [PyPI](https://pypi.org/project/ign-gpao-project-builder/):

    pip install ign-gpao-project-builder

## Exemple d'utilisation

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

    #print(project2.to_json())

    job6 = Job("job6", "touch file")
    job7 = Job("job7", "touch file", job6)
    project3 = Project("project3", [job6, job7], [project1, project2])

    #print(project3.to_json())

    builder = Builder([project1, project2])
    builder.add_project(project3)

    builder.save_as_json("project.json")
  
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
    
### Licence

Ce projet est sous licence CECILL-B (voir [LICENSE.md](https://github.com/ign-gpao/.github/blob/main/LICENSE.md)).

[![IGN](https://github.com/ign-gpao/.github/blob/main/images/logo_ign.png)](https://www.ign.fr)
