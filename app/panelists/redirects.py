# Copyright (c) 2018-2023 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Panelists Redirect Routes for Wait Wait Reports."""
from flask import Blueprint, url_for

from app.utility import redirect_url

blueprint = Blueprint("panelists_redirects", __name__)


@blueprint.route("/panelist")
@blueprint.route("/panelists")
def index():
    """View: Panelists Index Redirect."""
    return redirect_url(url_for("panelists.index"), status_code=301)


@blueprint.route("/panelist/aggregate_scores")
def aggregate_scores():
    """View: Panelists Aggregate Scores Report Redirect."""
    return redirect_url(url_for("panelists.aggregate_scores"), status_code=301)


@blueprint.route("/panelist/appearances_by_year")
def appearances_by_year():
    """View: Panelists Appearances By Year Report Redirect."""
    return redirect_url(url_for("panelists.appearances_by_year"), status_code=301)


@blueprint.route("/panelist/bluff_stats")
def bluff_stats():
    """View: Panelists Bluff the Listener Statistics Report Redirect."""
    return redirect_url(url_for("panelists.bluff_stats"), status_code=301)


@blueprint.route("/panelist/debut_by_year")
def debut_by_year():
    """View: Panelists Debut by Year Report Redirect."""
    return redirect_url(url_for("panelists.debut_by_year"), status_code=301)


@blueprint.route("/panelist/first_most_recent_appearances")
def first_most_recent_appearances():
    """View: Panelists First and Most Recent Appearances Report Redirect."""
    return redirect_url(
        url_for("panelists.first_most_recent_appearances"), status_code=301
    )


@blueprint.route("/panelist/gender_stats")
def gender_stats():
    """View: Panelists Statistics by Gender Report Redirect."""
    return redirect_url(url_for("panelists.gender_stats"), status_code=301)


@blueprint.route("/panelist/losing_streaks")
def losing_streaks():
    """View: Panelists Losing Streaks Report Redirect."""
    return redirect_url(url_for("panelists.losing_streaks"), status_code=301)


@blueprint.route("/panelist/panel_gender_mix")
@blueprint.route("/panelists/panel_gender_mix")
def panel_gender_mix():
    """View: Panel Gender Mix Report Redirect."""
    return redirect_url(url_for("shows.panel_gender_mix"), status_code=301)


@blueprint.route("/panelist/panelist_pvp_report")
@blueprint.route("/panelist/panelist_vs_panelist")
@blueprint.route("/panelist/pvp")
def pvp():
    """View: Panelist vs Panelist Report Redirect."""
    return redirect_url(url_for("panelists.panelist_pvp"), status_code=301)


@blueprint.route("/panelist/panelist_vs_panelist_scoring")
def panelist_vs_panelist_scoring():
    """View: Panelist vs Panelist Scoring Report Redirect."""
    return redirect_url(url_for("panelists.panelist_pvp_scoring"), status_code=301)


@blueprint.route("/panelist/rankings_summary")
def rankings_summary():
    """View: Panelists Rankings Summary Report Redirect."""
    return redirect_url(url_for("panelists.rankings_summary"), status_code=301)


@blueprint.route("/panelist/single_appearance")
def single_appearance():
    """View: Panelists Single Appearance Report Redirect."""
    return redirect_url(url_for("panelists.single_appearance"), status_code=301)


@blueprint.route("/panelist/stats_summary")
def stats_summary():
    """View: Panelists Statistics Summary Report Redirect."""
    return redirect_url(url_for("panelists.stats_summary"), status_code=301)


@blueprint.route("/panelist/win_streaks")
def win_streaks():
    """View: Panelists Index Redirect."""
    return redirect_url(url_for("panelists.win_streaks"), status_code=301)
