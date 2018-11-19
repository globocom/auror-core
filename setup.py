# encoding: utf-8

from setuptools import setup, find_packages

with open("version.txt") as version_file:
    version = version_file.read().strip()

setup(
    name="auror_core",
    version=version,
    description="Doing Jobs Dinamically with Azkaban",
    author="Big Data",
    author_email="bigdata@corp.globo.com",
    license='MIT',
    install_requires=[
        "jproperties",
        "pyaml"
    ],
    packages=find_packages(),
)
