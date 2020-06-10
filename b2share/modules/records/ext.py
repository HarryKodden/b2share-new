# -*- coding: utf-8 -*-
#
# This file is part of EUDAT B2Share.
# Copyright (C) 2016 University of Tuebingen, CERN.
# Copyright (C) 2015 University of Tuebingen.
#
# B2Share is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# B2Share is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with B2Share; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""B2share records extension"""

from __future__ import absolute_import, print_function


from __future__ import absolute_import, print_function

from invenio_files_rest.signals import file_deleted, file_uploaded
from invenio_indexer.signals import before_record_index

from . import config, indexer
from . tasks import update_record_files_async
from . triggers import register_triggers
from . errors import register_error_handlers

class B2ShareRecords(object):
    """B2SHARE extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        app.extensions['b2share'] = self
        self._register_signals(app)
        app.cli.add_command(b2records)
        register_triggers(app)
        register_error_handlers(app)

    def init_config(self, app):
        """Initialize configuration.

        Override configuration variables with the values in this package.
        """
        with_endpoints = app.config.get(
            'B2SHARE_ENDPOINTS_ENABLED', True)
        for k in dir(config):
            if k.startswith('B2SHARE_'):
                app.config.setdefault(k, getattr(config, k))
            elif k == 'SEARCH_UI_JSTEMPLATE_RESULTS':
                app.config['SEARCH_UI_JSTEMPLATE_RESULTS'] = getattr(
                    config, k)
            elif k == 'PIDSTORE_RECID_FIELD':
                app.config['PIDSTORE_RECID_FIELD'] = getattr(config, k)
            elif k == 'FILES_REST_PERMISSION_FACTORY':
                app.config['FILES_REST_PERMISSION_FACTORY'] =\
                        getattr(config, k)
            else:
                for n in ['RECORDS_REST_ENDPOINTS', 'RECORDS_UI_ENDPOINTS',
                          'RECORDS_REST_FACETS', 'RECORDS_REST_SORT_OPTIONS',
                          'RECORDS_REST_DEFAULT_SORT',
                          'RECORDS_FILES_REST_ENDPOINTS']:
                    if k == n and with_endpoints:
                        app.config.setdefault(n, {})
                        app.config[n].update(getattr(config, k))

    def _register_signals(self, app):
        """Register signals."""
        before_record_index.dynamic_connect(
            indexer.indexer_receiver,
            sender=app,
            index="records-record-v1.0.0")

        file_deleted.connect(update_record_files_async, weak=False)
        file_uploaded.connect(update_record_files_async, weak=False)


from invenio_records_rest.utils import PIDConverter
from invenio_indexer.signals import before_record_index
from invenio_records_rest import utils

from .views import create_blueprint
from .indexer import indexer_receiver
from .cli import b2records



class XXXB2ShareRecords(object):
    """B2Share Records extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        app.cli.add_command(b2records)
        app.extensions['b2share-records'] = self
        register_triggers(app)
        register_error_handlers(app)

        app.logger.info("Creating enpoints...")

        # Register records API blueprints
        endpoints = app.config['B2SHARE_RECORDS_REST_ENDPOINTS']
        for i in endpoints:
            app.logger.info("- Creating enpoint: {}".format(i))

        app.register_blueprint(create_blueprint(endpoints))

        @app.before_first_request
        def extend_default_endpoint_prefixes():
            """Fix the endpoint prefixes as ."""

            endpoint_prefixes = utils.build_default_endpoint_prefixes(endpoints)
            app.logger.info("- Fixing endpoint: {}".format(endpoint_prefixes))

            current_records_rest = app.extensions['invenio-records-rest']
            current_records_rest.default_endpoint_prefixes.update(
                endpoint_prefixes
            )

        before_record_index.connect(indexer_receiver, sender=app)
        app.url_map.converters['pid'] = PIDConverter


    def init_config(self, app):
        """Initialize configuration."""
        pass
