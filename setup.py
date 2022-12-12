import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="ign-gpao-project-builder",
    version=open("gpao/__init__.py").readlines()[-1].split()[-1].strip("\"'"),
    description="Write a json's GPAO file",
    long_description_content_type="text/markdown",
    long_description=README,
    url="https://github.com/ign-gpao/builder-python.git",
    author="Arnaud Birk",
    author_email="arnaud.birk@ign.fr",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["gpao"],
    include_package_data=True,
    install_requires=[
          'requests',
      ],
)
