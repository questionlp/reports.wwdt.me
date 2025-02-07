# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Panelists Redirect Routes for Wait Wait Reports."""

from flask import Blueprint, Response, url_for

from app.utility import redirect_url

blueprint = Blueprint("panelists_redirects", __name__)


@blueprint.route("/panelist")
@blueprint.route("/panelists")
def index() -> Response:
    """View: Index Redirect."""
    return redirect_url(url_for("panelists.index"), status_code=301)


@blueprint.route("/panelist/aggregate_scores")
def aggregate_scores() -> Response:
    """View: Panelists Aggregate Scores Report Redirect."""
    return redirect_url(url_for("panelists.aggregate_scores"), status_code=301)


@blueprint.route("/panelist/appearances_by_year")
def appearances_by_year() -> Response:
    """View: Appearances By Year Report Redirect."""
    return redirect_url(url_for("panelists.appearances_by_year"), status_code=301)


@blueprint.route("/panelist/bluff_stats")
@blueprint.route("/panelists/bluff-stats")
def bluff_the_listener_statistics() -> Response:
    """View: Panelists Bluff the Listener Statistics Report Redirect."""
    return redirect_url(
        url_for("panelists.bluff_the_listener_statistics"), status_code=301
    )


@blueprint.route("/panelists/bluff-stats-by-year")
def bluff_the_listener_statistics_by_year() -> Response:
    """View: Panelists Bluff the Listener Statistics by Year Report Redirect."""
    return redirect_url(
        url_for("panelists.bluff_the_listener_statistics_by_year"), status_code=301
    )


@blueprint.route("/panelist/debut_by_year")
@blueprint.route("/panelists/debut-by-year")
def debuts_by_year() -> Response:
    """View: Debuts by Year Report Redirect."""
    return redirect_url(url_for("panelists.debuts_by_year"), status_code=301)


@blueprint.route("/panelist/first_most_recent_appearances")
def first_most_recent_appearances() -> Response:
    """View: First and Most Recent Appearances Report Redirect."""
    return redirect_url(
        url_for("panelists.first_most_recent_appearances"), status_code=301
    )


@blueprint.route("/panelist/gender_stats")
@blueprint.route("/panelists/gender-stats")
def statistics_by_gender() -> Response:
    """View: Statistics by Gender Report Redirect."""
    return redirect_url(url_for("panelists.statistics_by_gender"), status_code=301)


@blueprint.route("/panelist/losing_streaks")
def losing_streaks() -> Response:
    """View: Losing Streaks Report Redirect."""
    return redirect_url(url_for("panelists.losing_streaks"), status_code=301)


@blueprint.route("/panelist/panel_gender_mix")
@blueprint.route("/panelists/panel_gender_mix")
def panel_gender_mix() -> Response:
    """View: Panel Gender Mix Report Redirect."""
    return redirect_url(url_for("shows.panel_gender_mix"), status_code=301)


@blueprint.route("/panelist/panelist_pvp_report")
@blueprint.route("/panelist/panelist_vs_panelist")
@blueprint.route("/panelist/pvp")
@blueprint.route("/panelists/panelist-pvp")
def panelist_vs_panelist() -> Response:
    """View: Panelist vs Panelist Report Redirect."""
    return redirect_url(url_for("panelists.panelist_vs_panelist"), status_code=301)


@blueprint.route("/panelists/panelist-pvp/all")
def panelist_vs_panelist_all() -> Response:
    """View: Panelist vs Panelist: All Report Redirect."""
    return redirect_url(url_for("panelists.panelist_vs_panelist_all"), status_code=301)


@blueprint.route("/panelist/panelist_vs_panelist_scoring")
def panelist_vs_panelist_scoring() -> Response:
    """View: Panelist vs Panelist Scoring Report Redirect."""
    return redirect_url(
        url_for("panelists.panelist_vs_panelist_scoring"), status_code=301
    )


@blueprint.route("/panelists/perfect-scores")
def perfect_score_counts() -> Response:
    """View: Perfect Score Counts Report Redirect."""
    return redirect_url(url_for("panelists.perfect_score_counts"), status_code=301)


@blueprint.route("/panelist/rankings_summary")
def rankings_summary() -> Response:
    """View: Rankings Summary Report Redirect."""
    return redirect_url(url_for("panelists.rankings_summary"), status_code=301)


@blueprint.route("/panelist/single_appearance")
def single_appearance() -> Response:
    """View: Single Appearance Report Redirect."""
    return redirect_url(url_for("panelists.single_appearance"), status_code=301)


@blueprint.route("/panelist/stats_summary")
@blueprint.route("/panelist/statistics_summary")
@blueprint.route("/panelists/stats-summary")
def statistics_summary() -> Response:
    """View: Statistics Summary Report Redirect."""
    return redirect_url(url_for("panelists.statistics_summary"), status_code=301)


@blueprint.route("/panelist/win_streaks")
def win_streaks() -> Response:
    """View: Panelists Index Redirect."""
    return redirect_url(url_for("panelists.win_streaks"), status_code=301)
