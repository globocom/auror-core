# encoding: utf-8

from setuptools import setup, find_packages

with open("version.txt") as version_file:
    version = version_file.read().strip()

setup(
    name="auror",
    version=version,
    description="criação de Jobs para o Azkaban",
    author="Big Data",
    author_email="bigdata@corp.globo.com",
    license='MIT',
    install_requires=[
        "jproperties"
    ],
    packages=find_packages(),
)
