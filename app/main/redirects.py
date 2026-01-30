# Copyright (c) 2018-2026 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Main Redirect Routes for Wait Wait Reports."""

from flask import Blueprint, Response, url_for

from app.utility import redirect_url

blueprint = Blueprint("main_redirects", __name__)


@blueprint.route("/favicon.ico")
def favicon() -> Response:
    """Redirect: /favicon.ico to /static/favicon.ico."""
    return redirect_url(url_for("static", filename="favicon.ico"), status_code=301)
