# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

install_requires = [
    'Django>=1.6,<=1.9',
    'unicodecsv>=0.14.1',
]

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-inline-csv-importer',
    version='0.1.3',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License',  # example license
    description='A simple django app to import admin inline data from CSV',
    long_description=README,
    url='https://github.com/zatan/django-inline-csv-importer',
    author='Edvinas Jurevicius',
    author_email='ikonitas@gmail.comth',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=install_requires,

)
