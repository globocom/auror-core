# encoding: utf-8

from setuptools import setup, find_packages

with open("version.txt") as version_file:
    version = version_file.read().strip()

setup(
    name="auror_core",
    version=version,
    long_description=open('README.md').read(),
    description="Doing Jobs Dinamically with Azkaban",
    author="Big Data",
    author_email="bigdata@corp.globo.com",
    license='MIT',
    install_requires=[
        "javaproperties==0.5.1",
        "pyaml==18.11.0"
    ],
    packages=find_packages(),
)
