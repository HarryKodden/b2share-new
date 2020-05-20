# -*- coding: utf-8 -*-

"""B2SHARE WSGI configuration."""

from __future__ import absolute_import, print_function

from .factory import create_app

# app holds both UI '/' plus API '/api' endpoints
app = create_app()
