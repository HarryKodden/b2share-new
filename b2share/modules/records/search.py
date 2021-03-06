# -*- coding: utf-8 -*-
#
# This file is part of EUDAT B2Share.
# Copyright (C) 2016 CERN.
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

"""Records search class and helpers."""

from elasticsearch_dsl.query import Bool, Q
from flask import has_request_context, request
from invenio_search.api import RecordsSearch, MinShouldMatch
from flask_security import current_user
from invenio_access.permissions import (
    superuser_access, ParameterizedActionNeed
)
from b2share.modules.access.permissions import StrictDynamicPermission

from .errors import AnonymousDepositSearch

def _in_draft_request():
    """Check if the current call is in a draft record request context.

    Returns:
        boolean: True when this function is called in a draft record request
                 context, else False.
    """
    return has_request_context() and 'drafts' in request.args


class B2ShareRecordsSearch(RecordsSearch):
    """Search class for records."""

    class MetaClass(type):
        @property
        def index(self):
            """Find the right index to search in."""
            if _in_draft_request():
                return 'deposits'
            return 'records'

        @property
        def doc_types(self):
            """Find the right document type to search for."""
            if _in_draft_request():
                return 'deposit'
            return 'record'

    class Meta(metaclass=MetaClass):
        """Default index and filter for record search."""

    def __init__(self, all_versions=False, **kwargs):
        """Initialize instance."""
        super(B2ShareRecordsSearch, self).__init__(**kwargs)

        return

        # FIXME: Code below break !!!!

        if _in_draft_request():
            if not current_user.is_authenticated:
                raise AnonymousDepositSearch()
            # super user can read all deposits
            if StrictDynamicPermission(superuser_access).can():
                return

            filters = [Q('term', **{'_deposit.owners': current_user.id})]

            from b2share.modules.deposit.permissions import list_readable_communities

            readable_communities = list_readable_communities(current_user.id)
            for publication_state in readable_communities.all:
                filters.append(Q('term', publication_state=publication_state))
            for community, publication_states in readable_communities.communities.items():
                for publication_state in publication_states:
                    filters.append(Bool(
                        must=[Q('term', publication_state=publication_state),
                              Q('term', community=str(community))],
                    ))


            # otherwise filter returned deposits
            self.query = Bool(
                must=self.query._proxied,
                should=filters,
                minimum_should_match=MinShouldMatch("0<1")
            )
        else:
            if not all_versions:
                # search for last record versions only
                filters = [Q('term', **{'_internal.is_last_version': True})]
                self.query = Bool(
                    must=self.query._proxied,
                    should=filters,
                    minimum_should_match=MinShouldMatch("0<1")
                )
