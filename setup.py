#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
from io import open

from setuptools import setup

try:
    from pypandoc import convert

    def read_md(f):
        return convert(f, 'rst').replace('\r', '')
except ImportError:
    print(
        "warning: pypandoc module not found, could not convert Markdown to RST"
    )

    def read_md(f):
        return open(f, 'r', encoding='utf-8').read()


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [
        dirpath
        for dirpath, dirnames, filenames in os.walk(package)
        if os.path.exists(os.path.join(dirpath, '__init__.py'))
    ]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [
        (dirpath.replace(package + os.sep, '', 1), filenames)
        for dirpath, dirnames, filenames in os.walk(package)
        if not os.path.exists(
            os.path.join(dirpath, '__init__.py')
        )
    ]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([
            os.path.join(base, filename) for filename in filenames
        ])
    return {package: filepaths}


def install_requirements():
    with open(os.path.join('requirements', 'install.txt')) as h:
        requirements = h.read().splitlines()
    return requirements


def testing_requirements():
    with open(os.path.join('requirements', 'testing.txt')) as h:
        requirements = h.read().splitlines()
    return requirements

version = "0.1.0"

setup(
    name='django-nimble',
    version=version,
    url='https://github.com/heoga/django-nimble',
    license='BSD',
    description='Nimble Project Management',
    long_description=read_md('README.md'),
    author='Karl Odie',
    author_email='karlodie@gmail.com',
    packages=get_packages('nimble'),
    package_data=get_package_data('nimble'),
    install_requires=install_requirements(),
    setup_requires=['pytest-runner>=2.9'],
    tests_require=testing_requirements(),
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
