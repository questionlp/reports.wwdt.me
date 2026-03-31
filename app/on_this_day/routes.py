# Copyright (c) 2018-2026 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Shows Routes for Wait Wait Reports."""

from datetime import date
from typing import Any

import mysql.connector
from flask import Blueprint, current_app, render_template, url_for

from app.utility import redirect_url

from .reports.details import retrieve_details

blueprint = Blueprint("on_this_day", __name__, template_folder="templates")


@blueprint.route("/")
def index() -> str:
    """View: On This Day Report."""
    if not current_app.config["app_settings"]["enable_on_this_day_report"]:
        return redirect_url(url_for("main.index"), status_code=302)

    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _date: date = date.today()
    _details: dict[str, list[dict[str, Any]]] = retrieve_details(
        month=_date.month, day=_date.day, database_connection=_database_connection
    )
    _database_connection.close()

    return render_template(
        "on_this_day/_report.html",
        date=_date,
        details=_details,
        specific_month_day=False,
    )


@blueprint.route("/<int:show_month>/<int:show_day>")
def month_day(show_month: int, show_day: int) -> str:
    """View: One This Day by Month and Day Report."""
    # Simple validation of month and day
    if not current_app.config["app_settings"]["enable_on_this_day_report"]:
        return redirect_url(url_for("main.index"), status_code=302)

    try:
        # Using 2004 as the year due to needing to a year that is a leap year.
        # The year value is not used as part of the queries or when rendering
        # the page.
        _temp_date: date = date(year=2004, month=show_month, day=show_day)

        _database_connection = mysql.connector.connect(**current_app.config["database"])
        _details: dict[str, list[dict[str, Any]]] = retrieve_details(
            month=show_month, day=show_day, database_connection=_database_connection
        )
        _database_connection.close()

        return render_template(
            "on_this_day/_report.html",
            date=_temp_date,
            details=_details,
            specific_month_day=True,
        )
    except ValueError:
        return redirect_url(url_for("on_this_day.index"), status_code=302)
