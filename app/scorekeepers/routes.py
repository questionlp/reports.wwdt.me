# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Scorekeepers Routes for Wait Wait Reports."""

import mysql.connector
from flask import Blueprint, current_app, render_template, request

from app.panelists.reports.appearances_by_year import retrieve_all_years

from .reports.appearances import (
    retrieve_appearance_summaries,
    retrieve_scorekeepers,
)
from .reports.appearances_by_year import (
    retrieve_all_appearance_counts,
    retrieve_all_appearance_counts_by_year,
)
from .reports.debut_by_year import retrieve_show_years, scorekeeper_debuts_by_year
from .reports.introductions import (
    retrieve_all_scorekeeper_introductions,
    retrieve_scorekeepers_with_introductions,
)
from .reports.show_apperances import retrieve_appearance_details

blueprint = Blueprint("scorekeepers", __name__, template_folder="templates")


@blueprint.route("/")
def index() -> str:
    """View: Index."""
    return render_template("scorekeepers/_index.html")


@blueprint.route("/appearance-summary")
def appearance_summary() -> str:
    """View: Appearance Summary Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _summaries = retrieve_appearance_summaries(database_connection=_database_connection)
    _database_connection.close()

    return render_template("scorekeepers/appearance-summary.html", summaries=_summaries)


@blueprint.route("/appearance-counts-by-year")
def appearance_counts_by_year() -> str:
    """View: Appearance Counts by Year Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _appearances = retrieve_all_appearance_counts_by_year(
        database_connection=_database_connection
    )
    _database_connection.close()

    return render_template(
        "scorekeepers/appearance-counts-by-year.html",
        years=list(_appearances.keys()),
        appearances=_appearances,
    )


@blueprint.route("/appearance-counts-by-year/grid")
def appearance_counts_by_year_grid() -> str:
    """View: Appearances by Year: Grid Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _scorekeepers = retrieve_all_appearance_counts(
        database_connection=_database_connection
    )
    _show_years = retrieve_all_years(database_connection=_database_connection)
    _database_connection.close()
    return render_template(
        "scorekeepers/appearance-counts-by-year-grid.html",
        scorekeepers=_scorekeepers,
        show_years=_show_years,
    )


@blueprint.route("/appearances-by-year", methods=["GET", "POST"])
def appearances_by_year() -> str:
    """View: Appearances by Year Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _scorekeepers = retrieve_scorekeepers(database_connection=_database_connection)
    _scorekeepers_dict = {
        scorekeeper["slug"]: scorekeeper["name"] for scorekeeper in _scorekeepers
    }
    _show_years = retrieve_show_years(database_connection=_database_connection)

    if request.method == "POST":
        _scorekeeper = "scorekeeper" in request.form and request.form["scorekeeper"]

        if _scorekeeper in _scorekeepers_dict:
            _scorekeeper_info = {
                "slug": _scorekeeper,
                "name": _scorekeepers_dict[_scorekeeper],
            }
            _appearances = retrieve_appearance_details(
                scorekeeper_slug=_scorekeeper,
                database_connection=_database_connection,
                include_decimal_scores=current_app.config["app_settings"][
                    "use_decimal_scores"
                ],
            )
            _database_connection.close()
            return render_template(
                "scorekeepers/appearances-by-year.html",
                scorekeepers=_scorekeepers,
                years=_show_years,
                scorekeeper_info=_scorekeeper_info,
                appearances=_appearances,
            )

        # No valid host returned
        _database_connection.close()
        return render_template(
            "scorekeepers/appearances-by-year.html",
            scorekeepers=_scorekeepers,
            years=_show_years,
            average_scores=None,
        )

    # Fallback for GET request
    _database_connection.close()
    return render_template(
        "scorekeepers/appearances-by-year.html",
        scorekeepers=_scorekeepers,
        years=_show_years,
    )


@blueprint.route("/scorekeeper-introductions")
def scorekeeper_introductions() -> str:
    """View: Scorekeeper Introductions Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _scorekeepers = retrieve_scorekeepers_with_introductions(
        database_connection=_database_connection
    )
    _introductions = retrieve_all_scorekeeper_introductions(
        database_connection=_database_connection
    )
    _database_connection.close()

    return render_template(
        "scorekeepers/scorekeeper-introductions.html",
        scorekeepers=_scorekeepers,
        introductions=_introductions,
    )


@blueprint.route("/debuts-by-year")
def debuts_by_year() -> str:
    """View: Debuts by Year Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _years = retrieve_show_years(database_connection=_database_connection)
    _debuts = scorekeeper_debuts_by_year(database_connection=_database_connection)
    _database_connection.close()
    return render_template(
        "scorekeepers/debuts-by-year.html", years=_years, debuts=_debuts
    )
