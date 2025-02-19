# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Guests Routes for Wait Wait Reports."""

import mysql.connector
from flask import Blueprint, current_app, render_template, request

from app.panelists.reports.debut_by_year import retrieve_show_years

from .reports.appearances_by_year import retrieve_appearances_by_year
from .reports.best_of_only import retrieve_best_of_only_guests
from .reports.most_appearances import guest_multiple_appearances
from .reports.scores import (
    retrieve_all_missing_scores,
    retrieve_all_scoring_exceptions,
    retrieve_all_three_pointers,
)
from .reports.wins_by_year import retrieve_wins_by_year

blueprint = Blueprint("guests", __name__, template_folder="templates")


@blueprint.route("/")
def index() -> str:
    """View: Guests Index."""
    return render_template("guests/_index.html")


@blueprint.route("/appearances-by-year", methods=["GET", "POST"])
def appearances_by_year() -> str:
    """View: Appearances by Year Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _show_years = retrieve_show_years(database_connection=_database_connection)

    if request.method == "POST":
        # Parse panelist dropdown selections
        _year = "year" in request.form and request.form["year"]
        try:
            year = int(_year)
        except ValueError:
            year = None

        if year not in _show_years:
            _database_connection.close()
            return render_template(
                "guests/appearances-by-year.html",
                show_years=_show_years,
                appearances=None,
            )

        _appearances = retrieve_appearances_by_year(
            year=year,
            database_connection=_database_connection,
        )
        if not _appearances:
            _database_connection.close()
            return render_template(
                "guests/appearances-by-year.html",
                show_years=_show_years,
                appearances=None,
            )

        _database_connection.close()
        return render_template(
            "guests/appearances-by-year.html",
            show_years=_show_years,
            year=year,
            appearances=_appearances,
        )

    # Fallback for GET request
    _database_connection.close()
    return render_template(
        "guests/appearances-by-year.html", show_years=_show_years, appearances=None
    )


@blueprint.route("/best-of-only-not-my-job-guests")
def best_of_only_not_my_job_guests() -> str:
    """View: Best Of Only Not My Job Guests Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _guests = retrieve_best_of_only_guests(database_connection=_database_connection)
    _database_connection.close()
    return render_template("guests/best-of-only-not-my-job-guests.html", guests=_guests)


@blueprint.route("/most-appearances")
def most_appearances() -> str:
    """View: Most Appearances Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _guests = guest_multiple_appearances(database_connection=_database_connection)
    _database_connection.close()
    return render_template("guests/most-appearances.html", guests=_guests)


@blueprint.route("/not-my-job-guests-missing-scores")
def not_my_job_guests_missing_scores() -> str:
    """View: Not My Job Guests with Missing Scores Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _guests = retrieve_all_missing_scores(database_connection=_database_connection)
    _database_connection.close()
    return render_template(
        "guests/not-my-job-guests-missing-scores.html", guests=_guests
    )


@blueprint.route("/not-my-job-scoring-exceptions")
def not_my_job_scoring_exceptions() -> str:
    """View: Not My Job Scoring Exceptions Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _exceptions = retrieve_all_scoring_exceptions(
        database_connection=_database_connection
    )
    _database_connection.close()
    return render_template(
        "guests/not-my-job-scoring-exceptions.html", exceptions=_exceptions
    )


@blueprint.route("/not-my-job-three-pointers")
def not_my_job_three_pointers() -> str:
    """View: Not My Job Three Pointers Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _three_pointers = retrieve_all_three_pointers(
        database_connection=_database_connection
    )
    _database_connection.close()
    return render_template(
        "guests/not-my-job-three-pointers.html", three_pointers=_three_pointers
    )


@blueprint.route("/wins-by-year", methods=["GET", "POST"])
def wins_by_year() -> str:
    """View: Wins by Year Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _show_years = retrieve_show_years(database_connection=_database_connection)

    if request.method == "POST":
        # Parse panelist dropdown selections
        _year = "year" in request.form and request.form["year"]
        try:
            year = int(_year)
        except ValueError:
            year = None

        if year not in _show_years:
            _database_connection.close()
            return render_template(
                "guests/wins-by-year.html",
                show_years=_show_years,
                appearances=None,
            )

        _appearances = retrieve_wins_by_year(
            year=year,
            database_connection=_database_connection,
        )
        if not _appearances:
            _database_connection.close()
            return render_template(
                "guests/wins-by-year.html",
                show_years=_show_years,
                appearances=None,
            )

        _database_connection.close()
        return render_template(
            "guests/wins-by-year.html",
            show_years=_show_years,
            year=year,
            appearances=_appearances,
        )

    # Fallback for GET request
    _database_connection.close()
    return render_template(
        "guests/wins-by-year.html", show_years=_show_years, appearances=None
    )
