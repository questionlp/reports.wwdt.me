# Copyright (c) 2018-2023 Linh Pham
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
def index():
    """View: Guests Index."""
    return render_template("guests/_index.html")


@blueprint.route("/best-of-only")
def best_of_only():
    """View: Guests Best Of Only Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _guests = retrieve_best_of_only_guests(database_connection=_database_connection)
    _database_connection.close()
    return render_template("guests/best-of-only.html", guests=_guests)


@blueprint.route("/most-appearances")
def most_appearances():
    """View: Guests Most Appearances Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _guests = guest_multiple_appearances(database_connection=_database_connection)
    _database_connection.close()
    return render_template("guests/most-appearances.html", guests=_guests)


@blueprint.route("/scoring-exceptions")
def scoring_exceptions():
    """View: Guests Scoring Exceptions Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _exceptions = retrieve_all_scoring_exceptions(
        database_connection=_database_connection
    )
    _database_connection.close()
    return render_template("guests/scoring-exceptions.html", exceptions=_exceptions)


@blueprint.route("/three-pointers")
def three_pointers():
    """View: Guests Three Pointers Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _three_pointers = retrieve_all_three_pointers(
        database_connection=_database_connection
    )
    _database_connection.close()
    return render_template("guests/three-pointers.html", three_pointers=_three_pointers)
