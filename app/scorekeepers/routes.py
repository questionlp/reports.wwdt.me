# Copyright (c) 2018-2023 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Scorekeepers Routes for Wait Wait Reports."""
import mysql.connector
from flask import Blueprint, current_app, render_template

from .reports.appearances import retrieve_appearance_summaries
from .reports.introductions import (
    retrieve_all_scorekeeper_introductions,
    retrieve_scorekeepers_with_introductions,
)

blueprint = Blueprint("scorekeepers", __name__, template_folder="templates")


@blueprint.route("/")
def index():
    """View: Scorekeepers Index."""
    return render_template("scorekeepers/_index.html")


@blueprint.route("/appearance-summary")
def appearance_summary():
    """View: Scorekeepers Appearance Summary Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _summaries = retrieve_appearance_summaries(database_connection=_database_connection)
    _database_connection.close()

    return render_template("scorekeepers/appearance-summary.html", summaries=_summaries)


@blueprint.route("/introductions")
def introductions():
    """View: Scorekeepers Introductions Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _scorekeepers = retrieve_scorekeepers_with_introductions(
        database_connection=_database_connection
    )
    _introductions = retrieve_all_scorekeeper_introductions(
        database_connection=_database_connection
    )
    _database_connection.close()

    return render_template(
        "scorekeepers/introductions.html",
        scorekeepers=_scorekeepers,
        introductions=_introductions,
    )
