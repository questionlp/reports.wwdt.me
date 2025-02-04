# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Hosts Redirect Routes for Wait Wait Reports."""

from flask import Blueprint, Response, url_for

from app.utility import redirect_url

blueprint = Blueprint("hosts_redirects", __name__)


@blueprint.route("/host")
@blueprint.route("/hosts")
def index() -> Response:
    """View: Index Redirect."""
    return redirect_url(url_for("hosts.index"), status_code=301)


@blueprint.route("/host/appearance_summary")
def appearance_summary() -> Response:
    """View: Appearance Summary Report Redirect."""
    return redirect_url(url_for("hosts.appearance_summary"), status_code=301)
