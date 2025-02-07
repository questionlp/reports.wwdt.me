# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Locations Routes for Wait Wait Reports."""

import mysql.connector
from flask import Blueprint, current_app, render_template

from .reports.average_scores import retrieve_average_scores_by_location
from .reports.home_vs_away import retrieve_location_home_vs_away

blueprint = Blueprint("locations", __name__, template_folder="templates")


@blueprint.route("/")
def index() -> str:
    """View: Index."""
    return render_template("locations/_index.html")


@blueprint.route("/average-scores-by-location")
def average_scores_by_location() -> str:
    """View: Average Scores by Location Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _locations = retrieve_average_scores_by_location(
        database_connection=_database_connection,
        use_decimal_scores=current_app.config["app_settings"]["use_decimal_scores"],
    )
    _database_connection.close()
    return render_template(
        "locations/average-scores-by-location.html", locations=_locations
    )


@blueprint.route("/home-vs-away")
def home_vs_away() -> str:
    """View: Show Locations: Home vs Away."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _show_counts = retrieve_location_home_vs_away(
        database_connection=_database_connection
    )
    return render_template("locations/home-vs-away.html", show_counts=_show_counts)
