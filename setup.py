#!/usr/bin/env python3

from setuptools import find_packages, setup


setup(
    name = 'django_tmapi',
    version = '1.0.0',
    description = 'Django app providing an implementation of the Topic Maps API 2.0',
    url = 'https://github.com/ajenhl/django-tmapi',
    author = 'Jamie Norrish',
    author_email = 'jamie@artefact.org.nz',
    license = 'Apache License, Version 2.0',
    packages = find_packages(),
    classifiers = [
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
    ]
)
