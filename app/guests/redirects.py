# Copyright (c) 2018-2024 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Guests Redirect Routes for Wait Wait Reports."""
from flask import Blueprint, Response, url_for

from app.utility import redirect_url

blueprint = Blueprint("guests_redirects", __name__)


@blueprint.route("/guest")
@blueprint.route("/guests")
def index() -> Response:
    """View: Guest Index."""
    return redirect_url(url_for("guests.index"), status_code=301)


@blueprint.route("/guest/best_of_only")
def best_of_only() -> Response:
    """View: Guests Best Of Only Report Redirect."""
    return redirect_url(url_for("guests.best_of_only"), status_code=301)


@blueprint.route("/guest/most_appearances")
def most_appearances() -> Response:
    """View: Guests Most Appearances Report."""
    return redirect_url(url_for("guests.most_appearances"), status_code=301)


@blueprint.route("/guest/scoring_exceptions")
def scoring_exceptions() -> Response:
    """View: Guests Scoring Exceptions Report."""
    return redirect_url(url_for("guests.scoring_exceptions"), status_code=301)


@blueprint.route("/guest/three_pointers")
def three_pointers() -> Response:
    """View: Guests Three Pointers Report."""
    return redirect_url(url_for("guests.three_pointers"), status_code=301)
