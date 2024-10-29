# Copyright (c) 2018-2024 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Locations Redirect Routes for Wait Wait Reports."""
from flask import Blueprint, Response, url_for

from app.utility import redirect_url

blueprint = Blueprint("locations_redirects", __name__)


@blueprint.route("/location")
@blueprint.route("/locations")
def index() -> Response:
    """View: Index Redirect."""
    return redirect_url(url_for("locations.index"), status_code=301)


@blueprint.route("/location/average_scores")
@blueprint.route("/locations/average-scores")
def average_scores_by_location() -> Response:
    """View: Average Score by Location Report Redirect."""
    return redirect_url(
        url_for("locations.average_scores_by_location"), status_code=301
    )
