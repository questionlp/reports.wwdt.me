# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2023 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""Shows Redirect Routes for Wait Wait Reports"""
from flask import Blueprint, url_for

from app.utility import redirect_url

blueprint = Blueprint("shows_redirects", __name__)


@blueprint.route("/show")
@blueprint.route("/shows")
def index():
    """View: Shows Index Redirect"""
    return redirect_url(url_for("shows.index"), status_code=301)


@blueprint.route("/show/all_shows")
def all_shows():
    """View: All Shows Report Redirect"""
    return redirect_url(url_for("shows.all_shows"), status_code=301)


@blueprint.route("/show/all_shows/asc")
@blueprint.route("/shows/all-shows/asc")
def all_shows_asc():
    """View: All Shows (Sort Ascending) Report Redirect"""
    return redirect_url(url_for("shows.all_shows"), status_code=301)


@blueprint.route("/show/all_shows/desc")
@blueprint.route("/shows/all-shows/desc")
def all_shows_desc():
    """View: All Shows (Sort Descending) Report Redirect"""
    return redirect_url(url_for("shows.all_shows", sort="desc"), status_code=301)


@blueprint.route("/show/all_women_panel")
def all_women_panel():
    """View: All Women Panel Report Redirect"""
    return redirect_url(url_for("shows.all_women_panel"), status_code=301)


@blueprint.route("/show/guest_host")
@blueprint.route("/show/guest_hosts")
@blueprint.route("/shows/guest-hosts")
def guest_host():
    """View: Shows with a Guest Hosts Report Redirect"""
    return redirect_url(url_for("shows.guest_host"), status_code=301)


@blueprint.route("/show/guest_scorekeeper")
@blueprint.route("/show/guest_scorekeepers")
@blueprint.route("/shows/guest-scorekeepers")
def guest_scorekeeper():
    """View: Shows with a Guest Scorekeeper Report Redirect"""
    return redirect_url(url_for("shows.guest_scorekeeper"), status_code=301)


@blueprint.route("/show/high_scoring")
def high_scoring():
    """View: High Scoring Shows Report Redirect"""
    return redirect_url(url_for("shows.high_scoring"), status_code=301)


@blueprint.route("/show/high_score_equal_sum_other_scores")
def highest_score_equals_sum_other_scores():
    """View: Highest Score Equals the Sum of Other Scores Report
    Redirect"""
    return redirect_url(
        url_for("shows.highest_score_equals_sum_other_scores"), status_code=301
    )


@blueprint.route("/show/lightning_round_end_three_way_tie")
def lightning_round_end_three_way_tie():
    """View: Lightning Round Ending in a Three-Way Tie Report
    Redirect"""
    return redirect_url(
        url_for("shows.lightning_round_ending_three_way_tie"), status_code=301
    )


@blueprint.route("/show/lightning_round_start_end_three_way_tie")
def lightning_round_start_end_three_way_tie():
    """View: Lightning Round Starting and Ending in a Three-Way Tie
    Report Redirect"""
    return redirect_url(
        url_for("shows.lightning_round_starting_ending_three_way_tie"), status_code=301
    )


@blueprint.route("/show/lighting_round_start_zero")
def lightning_round_start_zero_points():
    """View: Lightning Round Starting with Zero Points Report
    Redirect"""
    return redirect_url(
        url_for("shows.lightning_round_starting_zero_points"), status_code=301
    )


@blueprint.route("/show/lightning_round_zero_correct")
def lightning_round_zero_correct():
    """View: Lightning Round with Zero Correct Answers Report
    Redirect"""
    return redirect_url(url_for("shows.lightning_round_zero_correct"), status_code=301)


@blueprint.route("/show/low_scoring")
def low_scoring():
    """View: Low Scoring Shows Report Redirect"""
    return redirect_url(url_for("shows.low_scoring"), status_code=301)


@blueprint.route("/show/original_shows")
def original_shows():
    """View: Original Shows Report Redirect"""
    return redirect_url(url_for("shows.original_shows"), status_code=301)


@blueprint.route("/show/original_shows/asc")
@blueprint.route("/shows/original-shows/asc")
def original_shows_asc():
    """View: Original Shows (Sort Ascending) Report Redirect"""
    return redirect_url(url_for("shows.original_shows"), status_code=301)


@blueprint.route("/show/original_shows/desc")
@blueprint.route("/shows/original-shows/desc")
def original_shows_desc():
    """View: Original Shows (Sort Descending) Report Redirect"""
    return redirect_url(url_for("shows.original_shows", sort="desc"), status_code=301)


@blueprint.route("/show/panel_gender_mix")
def panel_gender_mix():
    """View: Panel Gender Mix Report Redirect"""
    return redirect_url(url_for("shows.panel_gender_mix"), status_code=301)


@blueprint.route("/show/search_multiple_panelists", methods=["GET", "POST"])
def search_multiple_panelists():
    """View: Search Shows by Multiple Panelists Report Redirect"""
    return redirect_url(url_for("shows.search_multiple_panelists"), status_code=301)


@blueprint.route("/show/counts_by_year")
@blueprint.route("/show/show_counts_by_year")
@blueprint.route("/shows/counts_by_year")
@blueprint.route("/shows/show_counts_by_year")
@blueprint.route("/shows/show-counts-by-year")
def counts_by_year():
    """View: Show Counts by Year Report Redirect"""
    return redirect_url(url_for("shows.counts_by_year"), status_code=301)
