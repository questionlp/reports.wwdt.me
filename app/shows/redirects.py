# Copyright (c) 2018-2024 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Shows Redirect Routes for Wait Wait Reports."""
from flask import Blueprint, Response, url_for

from app.utility import redirect_url

blueprint = Blueprint("shows_redirects", __name__)


@blueprint.route("/show")
@blueprint.route("/shows")
def index() -> Response:
    """View: Index Redirect."""
    return redirect_url(url_for("shows.index"), status_code=301)


@blueprint.route("/show/all_shows")
def all_shows() -> Response:
    """View: All Shows Report Redirect."""
    return redirect_url(url_for("shows.all_shows"), status_code=301)


@blueprint.route("/show/all_shows/asc")
@blueprint.route("/shows/all-shows/asc")
def all_shows_asc() -> Response:
    """View: All Shows (Sort Ascending) Report Redirect."""
    return redirect_url(url_for("shows.all_shows"), status_code=301)


@blueprint.route("/show/all_shows/desc")
@blueprint.route("/shows/all-shows/desc")
def all_shows_desc() -> Response:
    """View: All Shows (Sort Descending) Report Redirect."""
    return redirect_url(url_for("shows.all_shows", sort="desc"), status_code=301)


@blueprint.route("/show/all_women_panel")
def all_women_panel() -> Response:
    """View: All Women Panel Report Redirect."""
    return redirect_url(url_for("shows.all_women_panel"), status_code=301)


@blueprint.route("/shows/descriptions")
def show_descriptions() -> Response:
    """View: Show Descriptions Report Redirect."""
    return redirect_url(url_for("shows.show_descriptions"), status_code=301)


@blueprint.route("/show/guest_host")
@blueprint.route("/show/guest_hosts")
@blueprint.route("/shows/guest-host")
@blueprint.route("/shows/guest-hosts")
def shows_with_guest_host() -> Response:
    """View: Shows with a Guest Hosts Report Redirect."""
    return redirect_url(url_for("shows.shows_with_guest_host"), status_code=301)


@blueprint.route("/show/guest_scorekeeper")
@blueprint.route("/show/guest_scorekeepers")
@blueprint.route("/shows/guest-scorekeeper")
@blueprint.route("/shows/guest-scorekeepers")
def shows_with_guest_scorekeeper() -> Response:
    """View: Shows with a Guest Scorekeeper Report Redirect."""
    return redirect_url(url_for("shows.shows_with_guest_scorekeeper"), status_code=301)


@blueprint.route("/show/high_scoring")
@blueprint.route("/shows/high-scoring")
def high_scoring_shows() -> Response:
    """View: High Scoring Shows Report Redirect."""
    return redirect_url(url_for("shows.high_scoring_shows"), status_code=301)


@blueprint.route("/show/high_score_equal_sum_other_scores")
def highest_score_equals_sum_other_scores() -> Response:
    """View: Highest Score Equals the Sum of Other Scores Report Redirect."""
    return redirect_url(
        url_for("shows.highest_score_equals_sum_other_scores"), status_code=301
    )


@blueprint.route("/show/lightning_round_end_three_way_tie")
def lightning_round_ending_three_way_tie() -> Response:
    """View: Lightning Round Ending in a Three-Way Tie Report Redirect."""
    return redirect_url(
        url_for("shows.lightning_round_ending_three_way_tie"), status_code=301
    )


@blueprint.route("/show/lightning_round_start_end_three_way_tie")
def lightning_round_start_ending_three_way_tie() -> Response:
    """View: Lightning Round Starting and Ending in a Three-Way Tie Report Redirect."""
    return redirect_url(
        url_for("shows.lightning_round_starting_ending_three_way_tie"), status_code=301
    )


@blueprint.route("/show/lighting_round_start_zero")
def lightning_round_starting_zero_points() -> Response:
    """View: Lightning Round Starting with Zero Points Report Redirect."""
    return redirect_url(
        url_for("shows.lightning_round_starting_zero_points"), status_code=301
    )


@blueprint.route("/show/lightning_round_zero_correct")
def lightning_round_zero_correct():
    """View: Lightning Round with Zero Correct Answers Report Redirect."""
    return redirect_url(url_for("shows.lightning_round_zero_correct"), status_code=301)


@blueprint.route("/show/low_scoring")
@blueprint.route("/shows/low-scoring")
def low_scoring_shows() -> Response:
    """View: Low Scoring Shows Report Redirect."""
    return redirect_url(url_for("shows.low_scoring_shows"), status_code=301)


@blueprint.route("/shows/not-my-job-vs-bluffs")
def not_my_job_guests_vs_bluff_the_listener_win_ratios() -> Response:
    """View: Not My Job Guests vs Bluff the Listener Win Ratios Report Redirect."""
    return redirect_url(
        url_for("shows.not_my_job_guests_vs_bluff_the_listener_win_ratios"),
        status_code=301,
    )


@blueprint.route("/shows/notes")
def show_notes() -> Response:
    """View: Show Notes Report Redirect."""
    return redirect_url(url_for("shows.show_notes"), status_code=301)


@blueprint.route("/show/original_shows")
def original_shows() -> Response:
    """View: Original Shows Report Redirect."""
    return redirect_url(url_for("shows.original_shows"), status_code=301)


@blueprint.route("/show/original_shows/asc")
@blueprint.route("/shows/original-shows/asc")
def original_shows_asc() -> Response:
    """View: Original Shows (Sort Ascending) Report Redirect."""
    return redirect_url(url_for("shows.original_shows"), status_code=301)


@blueprint.route("/show/original_shows/desc")
@blueprint.route("/shows/original-shows/desc")
def original_shows_desc() -> Response:
    """View: Original Shows (Sort Descending) Report Redirect."""
    return redirect_url(url_for("shows.original_shows", sort="desc"), status_code=301)


@blueprint.route("/show/panel_gender_mix")
def panel_gender_mix() -> Response:
    """View: Panel Gender Mix Report Redirect."""
    return redirect_url(url_for("shows.panel_gender_mix"), status_code=301)


@blueprint.route("/shows/perfect-panelist-scores")
def shows_with_perfect_panelist_scores() -> Response:
    """View: Shows with Perfect Panelist Scores Report Redirect."""
    return redirect_url(
        url_for("shows.shows_with_perfect_panelist_scores"), status_code=301
    )


@blueprint.route("/show/search_multiple_panelists", methods=["GET", "POST"])
@blueprint.route("/shows/search-multiple-panelists", methods=["GET", "POST"])
def search_shows_by_multiple_panelists() -> Response:
    """View: Search Shows by Multiple Panelists Report Redirect."""
    return redirect_url(
        url_for("shows.search_shows_by_multiple_panelists"), status_code=301
    )


@blueprint.route("/show/counts_by_year")
@blueprint.route("/show/show_counts_by_year")
@blueprint.route("/shows/counts-by-year")
@blueprint.route("/shows/counts_by_year")
@blueprint.route("/shows/show_counts_by_year")
def show_counts_by_year() -> Response:
    """View: Show Counts by Year Report Redirect."""
    return redirect_url(url_for("shows.show_counts_by_year"), status_code=301)
