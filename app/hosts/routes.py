# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Hosts Routes for Wait Wait Reports."""

import mysql.connector
from flask import Blueprint, current_app, render_template, request

from app.panelists.reports.appearances_by_year import retrieve_all_years

from .reports.appearances import retrieve_appearance_summaries, retrieve_hosts
from .reports.appearances_by_year import (
    retrieve_all_appearance_counts,
    retrieve_all_appearance_counts_by_year,
)
from .reports.debut_by_year import host_debuts_by_year, retrieve_show_years
from .reports.show_appearances import retrieve_appearance_details

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


@blueprint.route("/appearance-counts-by-year")
def appearance_counts_by_year() -> str:
    """View: Appearance Counts by Year Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _appearances = retrieve_all_appearance_counts_by_year(
        database_connection=_database_connection
    )
    _database_connection.close()

    return render_template(
        "hosts/appearance-counts-by-year.html",
        years=list(_appearances.keys()),
        appearances=_appearances,
    )


@blueprint.route("/appearance-counts-by-year/grid")
def appearance_counts_by_year_grid() -> str:
    """View: Appearance Counts by Year: Grid Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _hosts = retrieve_all_appearance_counts(database_connection=_database_connection)
    _show_years = retrieve_all_years(database_connection=_database_connection)
    _database_connection.close()
    return render_template(
        "hosts/appearance-counts-by-year-grid.html",
        hosts=_hosts,
        show_years=_show_years,
    )


@blueprint.route("/appearances-by-year", methods=["GET", "POST"])
def appearances_by_year() -> str:
    """View: Appearances by Year Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _hosts = retrieve_hosts(database_connection=_database_connection)
    _hosts_dict = {host["slug"]: host["name"] for host in _hosts}
    _show_years = retrieve_show_years(database_connection=_database_connection)

    if request.method == "POST":
        _host = "host" in request.form and request.form["host"]

        if _host in _hosts_dict:
            _host_info = {"slug": _host, "name": _hosts_dict[_host]}
            _appearances = retrieve_appearance_details(
                host_slug=_host,
                database_connection=_database_connection,
            )
            _database_connection.close()
            return render_template(
                "hosts/appearances-by-year.html",
                hosts=_hosts,
                years=_show_years,
                host_info=_host_info,
                appearances=_appearances,
            )

        # Host not found
        _database_connection.close()
        return render_template(
            "hosts/appearances-by-year.html",
            hosts=_hosts,
            years=_show_years,
            average_scores=None,
        )

    # Fallback for GET request
    _database_connection.close()
    return render_template(
        "hosts/appearances-by-year.html", hosts=_hosts, years=_show_years
    )


@blueprint.route("/debuts-by-year")
def debuts_by_year() -> str:
    """View: Debuts by Year Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _years = retrieve_show_years(database_connection=_database_connection)
    _debuts = host_debuts_by_year(database_connection=_database_connection)
    _database_connection.close()
    return render_template("hosts/debuts-by-year.html", years=_years, debuts=_debuts)
