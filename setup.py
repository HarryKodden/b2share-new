# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 EUDAT.
#
# B2SHARE is free software; you can redistribute it and/or modify it under
# the terms of the MIT License; see LICENSE file for more details.

"""EUDAT Collaborative Data Infrastructure."""

import os, sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

readme = open('README.rst').read()

tests_require = [
    'check-manifest>=0.35',
    'coverage>=4.5.3',
    'isort>=4.3',
    'pydocstyle>=3.0.0',
    'pytest-cov>=2.7.1',
    'pytest-invenio>=1.3.1,<1.4.0',
    'pytest-pep8>=1.0.6',
    'pytest>=4.6.4,<5.0.0',
]

db_version = '>=1.0.5,<1.1.0'
search_version = '>=1.3.1,<1.4.0'

extras_require = {
    # Bundles
    'base': [
        'invenio-admin>=1.2.1,<1.3.0',
        'invenio-assets>=1.2.0,<1.3.0',
        'invenio-formatter>=1.0.3,<1.1.0',
        'invenio-logging>=1.3.0,<1.4.0',
        'invenio-mail>=1.0.2,<1.1.0',
        'invenio-rest>=1.2.1,<1.3.0',
        'invenio-theme>=1.3.0a3,<1.4.0',
    ],
    'auth': [
        'invenio-access>=1.4.1,<1.5.0',
        'invenio-accounts>=1.4.0a2,<1.5.0',
		'invenio-accounts-rest>=1.0.0a4',
        'invenio-oauth2server>=1.2.0,<1.3.0',
        'invenio-oauthclient>=1.2.1,<1.3.0',
        'invenio-userprofiles>=1.1.1,<1.2.0',
    ],
    'metadata': [
        'invenio-indexer>=1.1.1,<1.2.0',
        'invenio-jsonschemas>=1.1.0,<1.2.0',
        'invenio-oaiserver>=1.2.0,<1.3.0',
        'invenio-pidstore>=1.2.0,<1.3.0',
        'invenio-records-rest>=1.7.1,<1.8.0',
        'invenio-records-ui>=1.1.0,<1.2.0',
        'invenio-records>=1.3.1,<1.4.0',
        'invenio-search-ui>=2.0.0a2,<2.1.0',
		'invenio_pidrelations>=-1.0.0a6',
        'invenio-queues-1.0.0a2',
		'invenio-marc21>=1.0.0a9',
		'jsonresolver==0.2.1',
		'datacite>=1.0.1',
		'dcxml>=0.1.2',
		'doschema>=1.0.0a1',
    ],
    'files': [
        'invenio-files-rest>=1.2.0,<1.3.0',
        'invenio-iiif>=1.1.0,<1.2.0',
        'invenio-previewer>=1.2.1,<1.3.0',
        'invenio-records-files>=1.2.1,<1.3.0',
		'invenio_deposit>=1.0.0a11',
    ],
	'search': [
		'elasticsearch>=-7.6.0',
		'elasticsearch-dsl>=7.1.0',
	],
    # Database version
    'postgresql': [
        'invenio-db[postgresql,versioning]{}'.format(db_version),
    ],
    'mysql': [
        'invenio-db[mysql,versioning]{}'.format(db_version),
    ],
    'sqlite': [
        'invenio-db[versioning]{}'.format(db_version),
    ],
    # Elasticsearch version
    'elasticsearch5': [
        'invenio-search[elasticsearch5]{}'.format(search_version),
    ],
    'elasticsearch6': [
        'invenio-search[elasticsearch6]{}'.format(search_version),
    ],
    'elasticsearch7': [
        'invenio-search[elasticsearch7]{}'.format(search_version),
    ],
    # Docs and test dependencies
    'docs': [
        'Sphinx>=1.5.1',
    ],
	'flask': [
		'Flask>=1.1.2',
		'Flask-BabelEx>=0.9.4',
		'Flask-Caching>=1.8.0',
		'Flask-CeleryExt>=0.3.4',
		'Flask-Limiter>=1.1.0,<1.2.0',
		'Flask-Login<0.5.0',
		'Flask-Principal>=0.4.0',
	],
    'misc': [
        'nbconvert==4.1.0',
        'jupyter-client==6.1.7',
        'jupyter-core==4.6.3',
        'jupyterlab-pygments==0.1.1',
        'ipython==7.1.0',
        'traitlets==4.3.3',
    ],
	'uwsgi': [
		'Werkzeug==0.16.1',
	],
	'db': [
		'sqlalchemy<1.3.6',
	],
	'webdav': [
		'easywebdav2>=-1.3.0',
	],
	'b2handle': [
		'b2handle>=1.1.2',
	],
	'httplib': [
		'httplib2>=0.17.3'
	],
    'code-quality': [
        "coverage==5.1",
    ],
    'tests': tests_require,
}

extras_require['all'] = []
for name, reqs in extras_require.items():
    if name in ('sqlite', 'mysql', 'postgresql') \
            or name.startswith('elasticsearch'):
        continue
    extras_require['all'].extend(reqs)


setup_requires = [
    'pytest-runner>=3.0.0,<5',
]

install_requires = [
    'invenio-app>=1.3.0,<1.4.0',
    'invenio-base>=1.2.3,<1.3.0',
    'invenio-cache>=1.1.0,<1.2.0',
    'invenio-celery>=1.2.0,<1.3.0',
    'invenio-config>=1.0.3,<1.1.0',
    'invenio-i18n>=1.2.0,<1.3.0',
]

class PyTest(TestCommand):
    """PyTest Test."""

    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        """Init pytest."""
        TestCommand.initialize_options(self)
        self.pytest_args = []
        try:
            from ConfigParser import ConfigParser
        except ImportError:
            from configparser import ConfigParser
        config = ConfigParser()
        config.read('pytest.ini')
        self.pytest_args = config.get('pytest', 'addopts').split(' ')

    def finalize_options(self):
        """Finalize pytest."""
        TestCommand.finalize_options(self)
        if hasattr(self, '_test_args'):
            self.test_suite = ''
        else:
            self.test_args = []
            self.test_suite = True

    def run_tests(self):
        """Run tests."""
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

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
	extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
)
