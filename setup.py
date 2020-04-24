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
    kwargs['entry_points']['invenio_base.api_apps'].append('b2share_foo = b2share.modules.b2share_foo:B2SHARE_FOO')
    kwargs['entry_points']['invenio_base.blueprints'].append('b2share_foo = b2share.modules.b2share_foo.views:blueprint')
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
    url='https://github.com/EUDAT-B2SHARE/b2share',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'console_scripts': [
            'b2share = invenio_app.cli:cli',
        ],
        'invenio_base.apps': [
            'b2share_records = b2share.records:B2SHARE',
        ],
        'invenio_base.blueprints': [
            'b2share = b2share.theme.views:blueprint',
            'b2share_records = b2share.records.views:blueprint',
        ],
        'invenio_assets.webpack': [
            'b2share_theme = b2share.theme.webpack:theme',
        ],
        'invenio_config.module': [
            'b2share = b2share.config',
        ],
        'invenio_i18n.translations': [
            'messages = b2share',
        ],
        'invenio_base.api_apps': [
            'b2share = b2share.records:B2SHARE',
         ],
        'invenio_jsonschemas.schemas': [
            'b2share = b2share.records.jsonschemas'
        ],
        'invenio_search.mappings': [
            'records = b2share.records.mappings'
        ],
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
