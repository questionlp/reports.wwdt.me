# Copyright (c) 2018-2025 Linh Pham
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
@blueprint.route("/guests/best-of-only")
def best_of_only_not_my_job_guests() -> Response:
    """View: Best Of Only Not My Job Guests Report Redirect."""
    return redirect_url(
        url_for("guests.best_of_only_not_my_job_guests"), status_code=301
    )


@blueprint.route("/guest/most_appearances")
def most_appearances() -> Response:
    """View: Most Appearances Report."""
    return redirect_url(url_for("guests.most_appearances"), status_code=301)


@blueprint.route("/guest/scoring_exceptions")
@blueprint.route("/guests/scoring-exceptions")
def not_my_job_scoring_exceptions() -> Response:
    """View: Not My Job Scoring Exceptions Report."""
    return redirect_url(
        url_for("guests.not_my_job_scoring_exceptions"), status_code=301
    )


@blueprint.route("/guest/three_pointers")
@blueprint.route("/guests/three-pointers")
def not_my_job_three_pointers() -> Response:
    """View: Not My Job Three Pointers Report."""
    return redirect_url(url_for("guests.not_my_job_three_pointers"), status_code=301)
