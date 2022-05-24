# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""Locations Routes for Wait Wait Reports"""
from flask import Blueprint, current_app, render_template

import mysql.connector

from .reports.average_scores import retrieve_average_scores_by_location

blueprint = Blueprint("locations", __name__, template_folder="templates")


@blueprint.route("/")
def index():
    """View: Locations Index"""
    return render_template("locations/_index.html")


@blueprint.route("/average-scores")
def average_scores():
    """View: Locations Average Scores Report"""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _locations = retrieve_average_scores_by_location(
        database_connection=_database_connection
    )
    _database_connection.close()
    return render_template("locations/average-scores.html", locations=_locations)
