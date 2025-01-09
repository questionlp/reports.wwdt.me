# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Hosts Routes for Wait Wait Reports."""
import mysql.connector
from flask import Blueprint, current_app, render_template

from .reports.appearances import retrieve_appearance_summaries

blueprint = Blueprint("hosts", __name__, template_folder="templates")


@blueprint.route("/")
def index() -> str:
    """View: Index."""
    return render_template("hosts/_index.html")


@blueprint.route("/appearance-summary")
def appearance_summary() -> str:
    """View: Appearance Summary Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    summary = retrieve_appearance_summaries(database_connection=_database_connection)
    _database_connection.close()
    return render_template("hosts/appearance-summary.html", summary=summary)
