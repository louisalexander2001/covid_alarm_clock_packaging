#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 00:48:28 2020

@author: louisalexander
This is the setup script for the covid_alarm_clock package.
"""

import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="covid_alarm_clock_packaging", # Replace with your own username
    version="0.0.1",
    author="Louis Alexander",
    author_email="lbwa201@exeter.ac.uk",
    description="A smart browser based COVID alarm clock.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/louisalexander2001/covid_alarm_clock_packaging",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)