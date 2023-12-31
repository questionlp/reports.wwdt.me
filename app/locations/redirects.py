# Copyright (c) 2018-2023 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Locations Redirect Routes for Wait Wait Reports."""
from flask import Blueprint, url_for

from app.utility import redirect_url

blueprint = Blueprint("locations_redirects", __name__)


@blueprint.route("/location")
@blueprint.route("/locations")
def index():
    """View: Locations Index Redirect."""
    return redirect_url(url_for("locations.index"), status_code=301)


@blueprint.route("/location/average_scores")
def average_scores():
    """View: Locations Average Scores Report Redirect."""
    return redirect_url(url_for("locations.average_scores"), status_code=301)
