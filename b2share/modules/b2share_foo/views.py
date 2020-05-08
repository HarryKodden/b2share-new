# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 EUDAT.
#
# B2SHARE_FOO is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""MODULE FOO for EUDAT Collaborative Data Infrastructure."""

# TODO: This is an example file. Remove it if you do not need it, including
# the templates and static folders as well as the test case.

from flask import Blueprint, render_template
from flask_babelex import gettext as _

blueprint = Blueprint(
    'b2share_foo',
    __name__,
    template_folder='templates',
    static_folder='static',
)


@blueprint.route("/xxx")
def index():
    """Render a basic view."""
    return render_template(
        "b2share_foo/index.html",
        module_name=_('B2SHARE_FOO'))
