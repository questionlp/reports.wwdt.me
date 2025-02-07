# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Scorekeepers Redirect Routes for Wait Wait Reports."""

from flask import Blueprint, Response, url_for

from app.utility import redirect_url

blueprint = Blueprint("scorekeepers_redirects", __name__)


@blueprint.route("/scorekeeper")
@blueprint.route("/scorekeepers")
def index() -> Response:
    """View: Scorekeepers Index Redirect."""
    return redirect_url(url_for("scorekeepers.index"), status_code=301)


@blueprint.route("/scorekeeper/appearance_summary")
def appearance_summary() -> Response:
    """View: Scorekeepers Appearance Summary Report Redirect."""
    return redirect_url(url_for("scorekeepers.appearance_summary"), status_code=301)


@blueprint.route("/scorekeeper/introductions")
@blueprint.route("/scorekeepers/introductions")
def scorekeeper_introductions() -> Response:
    """View: Scorekeepers Introductions Report Redirect."""
    return redirect_url(
        url_for("scorekeepers.scorekeeper_introductions"), status_code=301
    )
