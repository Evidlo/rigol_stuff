#!/usr/bin/env python3


from setuptools import find_packages, setup

with open("README.md") as f:
    README = f.read()

version = {}
# manually read version from file
with open("rigol_stuff/version.py") as file:
    exec(file.read(), version)

setup(
    # some basic project information
    name="rigol_stuff",
    version=version["__version__"],
    license="GPL3",
    description="Example python project",
    long_description=README,
    long_description_content_type='text/markdown',
    author="Evan Widloski",
    author_email="evan_github@widloski.com",
    url="https://github.com/evidlo/rigol_stuff",
    # your project's pip dependencies
    install_requires=[
        "pyvisa",
        "pyvisa-py",
        "pyusb"
    ],
    include_package_data=True,
    # automatically look for subfolders with __init__.py
    packages=find_packages(),
    # if you want your code to be able to run directly from command line
)
