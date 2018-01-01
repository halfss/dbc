#!/usr/bin/env python2.7

from setuptools import setup, find_packages

setup(
        name="dbc",
        version='0.1',
        description="Data block chain",
        author="halfss",
        install_requires=[
                "tornado",
                "requests"
            ],
        scripts=[
            "bin/dbc_core",
            ],
        packages=find_packages(),
        data_files = [
            ('/etc/dbc', ['etc/dbc.conf',])
            ]
        )
