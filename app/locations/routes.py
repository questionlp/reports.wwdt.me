# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""Locations Routes for Wait Wait Reports"""
from flask import Blueprint, render_template

from .reports.average_scores import retrieve_average_scores_by_location

blueprint = Blueprint("locations", __name__)


@blueprint.route("/")
def index():
    """View: Locations Index"""
    return render_template("locations/_index.html")


@blueprint.route("/average-scores")
def average_scores():
    """View: Locations Average Scores Report"""
    _locations = retrieve_average_scores_by_location()
    return render_template("locations/average-scores.html", locations=_locations)
