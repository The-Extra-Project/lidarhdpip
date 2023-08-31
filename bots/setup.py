#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="bots",
    version= "0.1.0",
    description="package for scripts to deploy bot using discord.py",
    long_description_content_type="text/markdown",
    author="Dhruv Malik",
    packages= [
        "consumer", "Discord", "producer", "test"
    ]
)


