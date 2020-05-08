# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 EUDAT.
#
# B2SHARE is free software; you can redistribute it and/or modify it under
# the terms of the MIT License; see LICENSE file for more details.

"""EUDAT Collaborative Data Infrastructure."""

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()

packages = find_packages()

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('b2share', 'version.py'), 'rt') as fp:
	exec(fp.read(), g)
	version = g['__version__']

def my_setup(**kwargs):
	with open('entry_points.txt', 'r') as f:
		entry_point = None

		for line in [l.rstrip() for l in f]:

			if line.startswith('[') and line.endswith(']'):
				entry_point = line.lstrip('[').rstrip(']')

			else:
				if 'entry_points' not in kwargs:
					kwargs['entry_points'] = {}

				if entry_point not in kwargs['entry_points']:
					kwargs['entry_points'][entry_point] = []

				if entry_point and line > '':
					kwargs['entry_points'][entry_point].append(line)

	setup(**kwargs)
		
my_setup(
	name='b2share',
	version=version,
	description=__doc__,
	long_description=readme,
	keywords='b2share Invenio',
	license='MIT',
	author='EUDAT',
	author_email='info@eudat.eu',
	url='https://github.com/HarryKodden/b2share-new',
	packages=packages,
	zip_safe=False,
	include_package_data=True,
	platforms='any',
	entry_points={
	},
	classifiers=[
		'Environment :: Web Environment',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python',
		'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.6',
		'Development Status :: 3 - Alpha',
	],
)
