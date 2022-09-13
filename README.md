# IGN GPAO Project Builder

IGN GPAO Project Builder is a basic a builder for Json's GPAO project

## Installation

You can install the IGN GPAO Project Builder from [PyPI](https://pypi.org/project/ign-gpao-project-builder/):

    python -m pip install ign-gpao-project-builder

## How to use

IGN GPAO Project Builder is a small library named `ign-gpao-project-builder`

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
