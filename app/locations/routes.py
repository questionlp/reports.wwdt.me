# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Locations Routes for Wait Wait Reports."""

import mysql.connector
from flask import Blueprint, current_app, render_template, request

from app.panelists.reports.debut_by_year import retrieve_show_years

from .reports.average_scores import retrieve_average_scores_by_location
from .reports.home_vs_away import retrieve_location_home_vs_away
from .reports.recordings_by_year import retrieve_recording_counts_by_year
from .reports.show_recordings import (
    retrieve_location,
    retrieve_locations,
    retrieve_recording_details,
)

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


@blueprint.route("/recordings-by-year", methods=["GET", "POST"])
def recordings_by_year() -> str:
    """View: Recordings by Year Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _locations = retrieve_locations(database_connection=_database_connection)
    _show_years = retrieve_show_years(database_connection=_database_connection)

    if request.method == "POST":
        _location = "location" in request.form and request.form["location"]
        _year = "year" in request.form and request.form["year"]
        try:
            year = int(_year)
        except ValueError:
            year = None

        if year not in _show_years:
            _database_connection.close()
            return render_template(
                "locations/recordings-by-year.html",
                locations=_locations,
                years=_show_years,
                recordings=None,
            )

        _location_info = retrieve_location(
            location_slug=_location, database_connection=_database_connection
        )
        _recordings = retrieve_recording_details(
            location_slug=_location,
            year=_year,
            database_connection=_database_connection,
        )
        if not _recordings:
            _database_connection.close()
            return render_template(
                "locations/recordings-by-year.html",
                locations=_locations,
                location_info=_location_info,
                years=_show_years,
                recordings=None,
            )

        _database_connection.close()
        return render_template(
            "locations/recordings-by-year.html",
            locations=_locations,
            years=_show_years,
            location_info=_location_info,
            year=year,
            recordings=_recordings,
        )

    # Fallback for GET request
    _database_connection.close()
    return render_template(
        "locations/recordings-by-year.html",
        locations=_locations,
        years=_show_years,
        recordings=None,
    )


@blueprint.route("/recording-counts-by-year", methods=["GET", "POST"])
def recording_counts_by_year() -> str:
    """View: Recording Counts by Year Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _show_years = retrieve_show_years(database_connection=_database_connection)

    if request.method == "POST":
        _year = "year" in request.form and request.form["year"]
        try:
            year = int(_year)
        except ValueError:
            year = None

        if year not in _show_years:
            _database_connection.close()
            return render_template(
                "locations/recording-counts-by-year.html",
                show_years=_show_years,
                recordings=None,
            )

        _recordings = retrieve_recording_counts_by_year(
            year=year,
            database_connection=_database_connection,
        )
        if not _recordings:
            _database_connection.close()
            return render_template(
                "locations/recording-counts-by-year.html",
                show_years=_show_years,
                recordings=None,
            )

        _database_connection.close()
        return render_template(
            "locations/recording-counts-by-year.html",
            show_years=_show_years,
            year=year,
            recordings=_recordings,
        )

    # Fallback for GET request
    _database_connection.close()
    return render_template(
        "locations/recording-counts-by-year.html",
        show_years=_show_years,
        recordings=None,
    )
