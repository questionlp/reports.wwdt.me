# Copyright (c) 2018-2024 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Locations Routes for Wait Wait Reports."""
import mysql.connector
from flask import Blueprint, current_app, render_template

from .reports.average_scores import retrieve_average_scores_by_location

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
