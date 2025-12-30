# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Shows Routes for Wait Wait Reports."""

import mysql.connector
from flask import Blueprint, current_app, render_template, request

from .reports.all_men_panel import retrieve_shows_all_men_panel
from .reports.all_women_panel import retrieve_shows_all_women_panel
from .reports.guest_host import retrieve_shows_guest_host
from .reports.guest_host_scorekeeper import retrieve_shows_guest_host_scorekeeper
from .reports.guest_scorekeeper import retrieve_shows_guest_scorekeeper
from .reports.guests_vs_bluffs import retrieve_stats_totals
from .reports.guests_vs_bluffs_by_year import retrieve_stats_all_years
from .reports.info import retrieve_show_descriptions, retrieve_show_notes
from .reports.lightning_round import (
    shows_ending_with_three_way_tie,
    shows_lightning_round_answering_same_number_correct,
    shows_lightning_round_start_zero,
    shows_lightning_round_zero_correct,
    shows_starting_ending_three_way_tie,
    shows_starting_with_three_way_tie,
)
from .reports.panel_gender_mix import panel_gender_mix_breakdown
from .reports.panel_matching_initials import retrieve_shows_panelists_matching_initials
from .reports.scoring import (
    retrieve_shows_all_high_scoring,
    retrieve_shows_all_low_scoring,
    retrieve_shows_panelist_perfect_scores,
    retrieve_shows_panelist_score_sum_match,
)
from .reports.search_multiple_panelists import (
    retrieve_matching_one,
    retrieve_matching_three,
    retrieve_matching_two,
    retrieve_panelists,
)
from .reports.show_counts import retrieve_show_counts_by_year
from .reports.show_details import retrieve_all_best_of_shows as details_best_of_shows
from .reports.show_details import (
    retrieve_all_original_shows as details_all_original_shows,
)
from .reports.show_details import (
    retrieve_all_repeat_best_of_shows as details_repeat_best_of_shows,
)
from .reports.show_details import retrieve_all_repeat_shows as details_repeat_shows
from .reports.show_details import retrieve_all_shows as details_all_shows
from .reports.unique_best_of_bluff import (
    retrieve_unique_best_of_bluff_shows as unique_bluff_shows,
)

blueprint = Blueprint("shows", __name__, template_folder="templates")


@blueprint.route("/")
def index() -> str:
    """View: Index."""
    return render_template("shows/_index.html")


@blueprint.route("/all-shows")
def all_shows() -> str:
    """View: All Shows Report."""
    _ascending = True
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _shows = details_all_shows(database_connection=_database_connection)
    _database_connection.close()

    if "sort" in request.args:
        _sort = str(request.args["sort"])

        if _sort.lower() == "desc":
            _ascending = False

    if not _ascending:
        _shows.reverse()

    return render_template("shows/all-shows.html", shows=_shows, ascending=_ascending)


@blueprint.route("/all-men-panel")
def all_men_panel() -> str:
    """View: All Men Panel Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _shows = retrieve_shows_all_men_panel(
        database_connection=_database_connection,
    )
    _database_connection.close()

    return render_template("shows/all-men-panel.html", shows=_shows)


@blueprint.route("/all-women-panel")
def all_women_panel() -> str:
    """View: All Women Panel Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _shows = retrieve_shows_all_women_panel(
        database_connection=_database_connection,
    )
    _database_connection.close()

    return render_template("shows/all-women-panel.html", shows=_shows)


@blueprint.route("/best-of-shows")
def best_of_shows() -> str:
    """View: Best Of Shows Report."""
    _ascending = True
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _shows = details_best_of_shows(database_connection=_database_connection)
    _database_connection.close()

    if "sort" in request.args:
        _sort = str(request.args["sort"])

        if _sort.lower() == "desc":
            _ascending = False

    if not _ascending:
        _shows.reverse()

    return render_template(
        "shows/best-of-shows.html", shows=_shows, ascending=_ascending
    )


@blueprint.route("/best-of-shows-with-unique-bluff-segments")
def best_of_shows_with_unique_bluff() -> str:
    """View: Best Of Shows with Unique Bluff the Listener Segments Report."""
    _ascending = True
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _shows = unique_bluff_shows(database_connection=_database_connection)
    _database_connection.close()

    if "sort" in request.args:
        _sort = str(request.args["sort"])

        if _sort.lower() == "desc":
            _ascending = False

    if not _ascending:
        _shows.reverse()

    return render_template(
        "shows/best-of-shows-with-unique-bluff-segments.html",
        shows=_shows,
        ascending=_ascending,
    )


@blueprint.route("/high-scoring-shows")
def high_scoring_shows() -> str:
    """View: High Scoring Shows Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _shows = retrieve_shows_all_high_scoring(
        database_connection=_database_connection,
    )
    _database_connection.close()

    return render_template("shows/high-scoring-shows.html", shows=_shows)


@blueprint.route("/highest-score-equals-sum-other-scores")
def highest_score_equals_sum_other_scores() -> str:
    """View: Highest Score Equals the Sum of Other Scores Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _shows = retrieve_shows_panelist_score_sum_match(
        database_connection=_database_connection,
    )
    _database_connection.close()

    return render_template(
        "shows/highest-score-equals-sum-other-scores.html", shows=_shows
    )


@blueprint.route("/lightning-round-answering-same-number-correct")
def lightning_round_answering_same_number_correct() -> str:
    """View: Lightning Fill In The Blank Panelists Answering the Same Number of Questions Correct."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _shows = shows_lightning_round_answering_same_number_correct(
        database_connection=_database_connection,
    )
    _database_connection.close()

    return render_template(
        "shows/lightning-round-answering-same-number-correct.html", shows=_shows
    )


@blueprint.route("/lightning-round-ending-three-way-tie")
def lightning_round_ending_three_way_tie() -> str:
    """View: Lightning Fill In The Blank Ending in a Three-Way Tie Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _shows = shows_ending_with_three_way_tie(
        database_connection=_database_connection,
    )
    _database_connection.close()

    return render_template(
        "shows/lightning-round-ending-three-way-tie.html", shows=_shows
    )


@blueprint.route("/lightning-round-starting-ending-three-way-tie")
def lightning_round_starting_ending_three_way_tie() -> str:
    """View: Lightning Fill In The Blank Starting and Ending in a Three-Way Tie Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _shows = shows_starting_ending_three_way_tie(
        database_connection=_database_connection,
    )
    _database_connection.close()

    return render_template(
        "shows/lightning-round-starting-ending-three-way-tie.html", shows=_shows
    )


@blueprint.route("/lightning-round-starting-three-way-tie")
def lightning_round_starting_three_way_tie() -> str:
    """View: Lightning Fill In The Blank Starting with a Three-Way Tie Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _shows = shows_starting_with_three_way_tie(
        database_connection=_database_connection,
    )
    _database_connection.close()

    return render_template(
        "shows/lightning-round-starting-three-way-tie.html", shows=_shows
    )


@blueprint.route("/lightning-round-starting-zero-points")
def lightning_round_starting_zero_points() -> str:
    """View: Lightning Fill In The Blank Starting with Zero Points Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _shows = shows_lightning_round_start_zero(
        database_connection=_database_connection,
    )
    _database_connection.close()

    return render_template(
        "shows/lightning-round-starting-zero-points.html", shows=_shows
    )


@blueprint.route("/lightning-round-zero-correct")
def lightning_round_zero_correct() -> str:
    """View: Lightning Fill In The Blank with Zero Correct Answers Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _shows = shows_lightning_round_zero_correct(
        database_connection=_database_connection,
    )
    _database_connection.close()

    return render_template("shows/lightning-round-zero-correct.html", shows=_shows)


@blueprint.route("/low-scoring-shows")
def low_scoring_shows() -> str:
    """View: Low Scoring Shows Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _shows = retrieve_shows_all_low_scoring(
        database_connection=_database_connection,
    )
    _database_connection.close()

    return render_template("shows/low-scoring-shows.html", shows=_shows)


@blueprint.route("/not-my-job-guests-vs-bluff-the-listener-win-ratios")
def not_my_job_guests_vs_bluff_the_listener_win_ratios() -> str:
    """View: Not My Job Guests vs Bluff the Listener Win Ratios by Year Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _stats_years = retrieve_stats_all_years(database_connection=_database_connection)
    _stats_totals = retrieve_stats_totals(database_connection=_database_connection)
    _database_connection.close()

    _stats = {}
    if _stats_years and _stats_totals:
        _stats.update(_stats_years)
        _stats.update(_stats_totals)

    return render_template(
        "shows/not-my-job-guests-vs-bluff-the-listener-win-ratios.html",
        years=list(_stats_years.keys()),
        stats=_stats,
    )


@blueprint.route("/original-shows")
def original_shows() -> str:
    """View: Original Shows Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _shows = details_all_original_shows(database_connection=_database_connection)
    _database_connection.close()

    _ascending = True
    if "sort" in request.args:
        _sort = str(request.args["sort"])

        if _sort.lower() == "desc":
            _ascending = False

    if not _ascending:
        _shows.reverse()

    return render_template(
        "shows/original-shows.html", shows=_shows, ascending=_ascending
    )


@blueprint.route("/panel-gender-mix")
def panel_gender_mix() -> str:
    """View: Panel Gender Mix Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _mix = panel_gender_mix_breakdown(database_connection=_database_connection)
    _database_connection.close()

    return render_template("shows/panel-gender-mix.html", panel_gender_mix=_mix)


@blueprint.route("/repeat-best-of-shows")
def repeat_best_of_shows() -> str:
    """View: Repeat Best Of Shows Report."""
    _ascending = True
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _shows = details_repeat_best_of_shows(database_connection=_database_connection)
    _database_connection.close()

    if "sort" in request.args:
        _sort = str(request.args["sort"])

        if _sort.lower() == "desc":
            _ascending = False

    if not _ascending:
        _shows.reverse()

    return render_template(
        "shows/repeat-best-of-shows.html", shows=_shows, ascending=_ascending
    )


@blueprint.route("/repeat-shows")
def repeat_shows() -> str:
    """View: Repeat Shows Report."""
    _ascending = True
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _shows = details_repeat_shows(database_connection=_database_connection)
    _database_connection.close()

    if "sort" in request.args:
        _sort = str(request.args["sort"])

        if _sort.lower() == "desc":
            _ascending = False

    if not _ascending:
        _shows.reverse()

    return render_template(
        "shows/repeat-shows.html", shows=_shows, ascending=_ascending
    )


@blueprint.route("/search-shows-by-multiple-panelists", methods=["GET", "POST"])
def search_shows_by_multiple_panelists() -> str:
    """View: Search Shows by Multiple Panelists Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _panelists = retrieve_panelists(database_connection=_database_connection)

    if request.method == "POST":
        # Parse panelist dropdown selections and checkboxes
        _panelist_1 = "panelist_1" in request.form and request.form["panelist_1"]
        _panelist_2 = "panelist_2" in request.form and request.form["panelist_2"]
        _panelist_3 = "panelist_3" in request.form and request.form["panelist_3"]
        _best_of = "best_of" in request.form and request.form["best_of"] == "on"
        _repeats = "repeats" in request.form and request.form["repeats"] == "on"

        # Create a set of panelist values to de-duplicate values
        # deduped_panelists = set([_panelist_1, _panelist_2, _panelist_3])
        deduped_panelists = {_panelist_1, _panelist_2, _panelist_3}

        # Remove any empty values
        if "" in deduped_panelists:
            deduped_panelists.remove("")

        if None in deduped_panelists:
            deduped_panelists.remove(None)

        if len(deduped_panelists) > 0 and deduped_panelists <= _panelists.keys():
            # Revert set back to list
            _panelist_values = list(deduped_panelists)
            _shows = []
            if len(_panelist_values) == 3:
                _shows = retrieve_matching_three(
                    database_connection=_database_connection,
                    panelist_slug_1=_panelist_values[0],
                    panelist_slug_2=_panelist_values[1],
                    panelist_slug_3=_panelist_values[2],
                    include_best_of=_best_of,
                    include_repeats=_repeats,
                )
            elif len(_panelist_values) == 2:
                _shows = retrieve_matching_two(
                    database_connection=_database_connection,
                    panelist_slug_1=_panelist_values[0],
                    panelist_slug_2=_panelist_values[1],
                    include_best_of=_best_of,
                    include_repeats=_repeats,
                )
            elif len(_panelist_values) == 1:
                _shows = retrieve_matching_one(
                    database_connection=_database_connection,
                    panelist_slug_1=_panelist_values[0],
                    include_best_of=_best_of,
                    include_repeats=_repeats,
                )

            _database_connection.close()
            if _shows:
                return render_template(
                    "shows/search-shows-by-multiple-panelists.html",
                    panelists=_panelists,
                    shows=_shows,
                )

            return render_template(
                "shows/search-shows-by-multiple-panelists.html",
                panelists=_panelists,
                shows=None,
            )

        # Fallback for no valid panelist(s) selected
        _database_connection.close()
        return render_template(
            "shows/search-shows-by-multiple-panelists.html",
            panelists=_panelists,
            shows=None,
        )

    # Fallback for GET request
    _database_connection.close()
    return render_template(
        "shows/search-shows-by-multiple-panelists.html",
        panelists=_panelists,
        shows=None,
    )


@blueprint.route("/show-counts-by-year")
def show_counts_by_year() -> str:
    """View: Show Counts by Year Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _counts = retrieve_show_counts_by_year(database_connection=_database_connection)
    _database_connection.close()

    return render_template("shows/show-counts-by-year.html", show_counts=_counts)


@blueprint.route("/show-descriptions")
def show_descriptions() -> str:
    """View: Show Descriptions."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _descriptions = retrieve_show_descriptions(database_connection=_database_connection)
    _database_connection.close()

    return render_template("shows/show-descriptions.html", descriptions=_descriptions)


@blueprint.route("/show-notes")
def show_notes() -> str:
    """View: Show Notes."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _notes = retrieve_show_notes(database_connection=_database_connection)
    _database_connection.close()

    return render_template("shows/show-notes.html", notes=_notes)


@blueprint.route("/shows-with-guest-host")
def shows_with_guest_host() -> str:
    """View: Shows with a Guest Host Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _shows = retrieve_shows_guest_host(database_connection=_database_connection)
    _database_connection.close()

    return render_template("shows/shows-with-guest-host.html", shows=_shows)


@blueprint.route("/shows-with-guest-host-scorekeeper")
def shows_with_guest_host_scorekeeper() -> str:
    """View: Shows with a Guest Host Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _shows = retrieve_shows_guest_host_scorekeeper(
        database_connection=_database_connection
    )
    _database_connection.close()

    return render_template("shows/shows-with-guest-host-scorekeeper.html", shows=_shows)


@blueprint.route("/shows-with-guest-scorekeeper")
def shows_with_guest_scorekeeper() -> str:
    """View: Shows with a Guest Scorekeeper Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _shows = retrieve_shows_guest_scorekeeper(database_connection=_database_connection)
    _database_connection.close()

    return render_template("shows/shows-with-guest-scorekeeper.html", shows=_shows)


@blueprint.route("/shows-with-panelists-matching-initials")
def shows_with_panelists_matching_initials() -> str:
    """View: Shows with Panelists Having Matching Initials."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _shows = retrieve_shows_panelists_matching_initials(
        database_connection=_database_connection
    )
    _database_connection.close()

    return render_template(
        "shows/shows-with-panelists-matching-initials.html", shows=_shows
    )


@blueprint.route("/shows-with-perfect-panelist-scores")
def shows_with_perfect_panelist_scores() -> str:
    """View: Shows with Perfect Panelist Scores Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _shows = retrieve_shows_panelist_perfect_scores(
        database_connection=_database_connection,
    )
    _database_connection.close()

    return render_template(
        "shows/shows-with-perfect-panelist-scores.html", shows=_shows
    )
