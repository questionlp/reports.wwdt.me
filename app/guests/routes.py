# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Guests Routes for Wait Wait Reports."""
import mysql.connector
from flask import Blueprint, current_app, render_template

from .reports.best_of_only import retrieve_best_of_only_guests
from .reports.most_appearances import guest_multiple_appearances
from .reports.scores import retrieve_all_scoring_exceptions, retrieve_all_three_pointers

blueprint = Blueprint("guests", __name__, template_folder="templates")


@blueprint.route("/")
def index() -> str:
    """View: Guests Index."""
    return render_template("guests/_index.html")


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
