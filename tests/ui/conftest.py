# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 EUDAT.
#
# B2SHARE is free software; you can redistribute it and/or modify it under
# the terms of the MIT License; see LICENSE file for more details.

"""Pytest fixtures and plugins for the UI application."""

from __future__ import absolute_import, print_function

import pytest

from b2share.factory import create_app as b2share_ui

@pytest.fixture(scope='module')
def create_app():
    """Create test app."""
    return b2share_ui()
    