# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""Guests Redirect Routes for Wait Wait Reports"""
from flask import Blueprint, url_for

from app.utility import redirect_url

blueprint = Blueprint("guests_redirects", __name__)


@blueprint.route("/guest")
def index():
    """View: Guest Index"""
    return redirect_url(url_for("guests.index"), status_code=301)


@blueprint.route("/guest/best_of_only")
def best_of_only():
    """View: Guests Best Of Only Report Redirect"""
    return redirect_url(url_for("guests.best_of_only"), status_code=301)


@blueprint.route("/guest/most_appearances")
def most_appearances():
    """View: Guests Most Appearances Report"""
    return redirect_url(url_for("guests.most_appearances"), status_code=301)


@blueprint.route("/guest/scoring_exceptions")
def scoring_exceptions():
    """View: Guests Scoring Exceptions Report"""
    return redirect_url(url_for("guests.scoring_exceptions"), status_code=301)


@blueprint.route("/guest/three_pointers")
def three_pointers():
    """View: Guests Three Pointers Report"""
    return redirect_url(url_for("guests.three_pointers"), status_code=301)
