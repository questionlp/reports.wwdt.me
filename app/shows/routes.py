# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""Shows Routes for Wait Wait Reports"""
from typing import Optional

from flask import Blueprint, current_app, render_template, request
import mysql.connector

from .reports.all_women_panel import retrieve_shows_all_women_panel
from .reports.show_counts import retrieve_show_counts_by_year
from .reports.guest_host import retrieve_shows_guest_host
from .reports.guest_scorekeeper import retrieve_shows_guest_scorekeeper
from .reports.lightning_round import (
    shows_ending_with_three_way_tie,
    shows_lightning_round_start_zero,
    shows_lightning_round_zero_correct,
    shows_starting_ending_three_way_tie,
    shows_starting_with_three_way_tie,
)
from .reports.scoring import (
    retrieve_shows_all_high_scoring,
    retrieve_shows_all_low_scoring,
    retrieve_shows_panelist_perfect_scores,
    retrieve_shows_panelist_score_sum_match,
)
from .reports.search_mutliple_panelists import (
    retrieve_panelists,
    retrieve_matching_one,
    retrieve_matching_two,
    retrieve_matching_three,
)
from .reports.show_details import (
    retrieve_all_shows as details_all_shows,
    retrieve_all_original_shows as details_all_original_shows,
)
from .reports.panel_gender_mix import panel_gender_mix_breakdown

blueprint = Blueprint("shows", __name__, template_folder="templates")


@blueprint.route("/")
def index():
    """View: Shows Index"""
    return render_template("shows/_index.html")


@blueprint.route("/all-shows")
def all_shows():
    """View: All Shows Report"""
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


@blueprint.route("/all-women-panel")
def all_women_panel():
    """View: All Women Panel Report"""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _shows = retrieve_shows_all_women_panel(database_connection=_database_connection)
    _database_connection.close()

    return render_template("shows/all-women-panel.html", shows=_shows)


@blueprint.route("/counts-by-year")
def counts_by_year():
    """View: Show Counts by Year Report"""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _counts = retrieve_show_counts_by_year(database_connection=_database_connection)
    _database_connection.close()

    return render_template("shows/counts-by-year.html", show_counts=_counts)


@blueprint.route("/guest-host")
def guest_host():
    """View: Shows with a Guest Host Report"""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _shows = retrieve_shows_guest_host(database_connection=_database_connection)
    _database_connection.close()

    return render_template("shows/guest-host.html", shows=_shows)


@blueprint.route("/guest-scorekeeper")
def guest_scorekeeper():
    """View: Shows with a Guest Scorekeeper Report"""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _shows = retrieve_shows_guest_scorekeeper(database_connection=_database_connection)
    _database_connection.close()

    return render_template("shows/guest-scorekeeper.html", shows=_shows)


@blueprint.route("/high-scoring")
def high_scoring():
    """View: High Scoring Shows Report"""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _shows = retrieve_shows_all_high_scoring(database_connection=_database_connection)
    _database_connection.close()

    return render_template("shows/high-scoring.html", shows=_shows)


@blueprint.route("/highest-score-equals-sum-other-scores")
def highest_score_equals_sum_other_scores():
    """View: Highest Score Equals the Sum of Other Scores Report"""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _shows = retrieve_shows_panelist_score_sum_match(
        database_connection=_database_connection
    )
    _database_connection.close()

    return render_template(
        "shows/highest-score-equals-sum-other-scores.html", shows=_shows
    )


@blueprint.route("/lightning-round-ending-three-way-tie")
def lightning_round_ending_three_way_tie():
    """View: Lightning Round Ending in a Three-Way Tie Report"""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _shows = shows_ending_with_three_way_tie(database_connection=_database_connection)
    _database_connection.close()

    return render_template(
        "shows/lightning-round-ending-three-way-tie.html", shows=_shows
    )


@blueprint.route("/lightning-round-starting-ending-three-way-tie")
def lightning_round_starting_ending_three_way_tie():
    """View: Lightning Round Starting and Ending in a Three-Way Tie
    Report"""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _shows = shows_starting_ending_three_way_tie(
        database_connection=_database_connection
    )
    _database_connection.close()

    return render_template(
        "shows/lightning-round-starting-ending-three-way-tie.html", shows=_shows
    )


@blueprint.route("/lightning-round-starting-three-way-tie")
def lightning_round_starting_three_way_tie():
    """View: Lightning Round Starting with a Three-Way Tie Report"""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _shows = shows_starting_with_three_way_tie(database_connection=_database_connection)
    _database_connection.close()

    return render_template(
        "shows/lightning-round-starting-three-way-tie.html", shows=_shows
    )


@blueprint.route("/lightning-round-starting-zero-points")
def lightning_round_starting_zero_points():
    """View: Lightning Round Starting with Zero Points Report"""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _shows = shows_lightning_round_start_zero(database_connection=_database_connection)
    _database_connection.close()

    return render_template(
        "shows/lightning-round-starting-zero-points.html", shows=_shows
    )


@blueprint.route("/lightning-round-zero-correct")
def lightning_round_zero_correct():
    """View: Lightning Round with Zero Correct Answers Report"""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _shows = shows_lightning_round_zero_correct(
        database_connection=_database_connection
    )
    _database_connection.close()

    return render_template("shows/lightning-round-zero-correct.html", shows=_shows)


@blueprint.route("/low-scoring")
def low_scoring():
    """View: Low Scoring Shows Report"""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _shows = retrieve_shows_all_low_scoring(database_connection=_database_connection)
    _database_connection.close()

    return render_template("shows/low-scoring.html", shows=_shows)


@blueprint.route("/original-shows")
def original_shows():
    """View: Original Shows Report"""
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
def panel_gender_mix(gender: Optional[str] = "female"):
    """View: Shows Panel Gender Mix Report"""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _gender_tag = gender[0].upper()
    _mix = panel_gender_mix_breakdown(
        database_connection=_database_connection, gender=gender
    )
    _database_connection.close()

    return render_template(
        "shows/panel-gender-mix.html", panel_gender_mix=_mix, gender=_gender_tag
    )


@blueprint.route("/perfect-panelist-scores")
def perfect_panelist_scores():
    """View: Shows with Perfect Panelist Scores Report"""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _shows = retrieve_shows_panelist_perfect_scores(
        database_connection=_database_connection
    )
    _database_connection.close()

    return render_template("shows/perfect-panelist-scores.html", shows=_shows)


@blueprint.route("/search-multiple-panelists", methods=["GET", "POST"])
def search_multiple_panelists():
    """View: Search Shows by Multiple Panelists Report"""
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
        deduped_panelists = set([_panelist_1, _panelist_2, _panelist_3])

        # Remove any empty values
        if "" in deduped_panelists:
            deduped_panelists.remove("")

        if None in deduped_panelists:
            deduped_panelists.remove(None)

        if len(deduped_panelists) > 0 and deduped_panelists <= _panelists.keys():
            # Revert set back to list
            _panelist_values = list(deduped_panelists)
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
            return render_template(
                "shows/search-multiple-panelists.html",
                panelists=_panelists,
                shows=_shows,
            )

        # Fallback for no valid panelist(s) selected
        _database_connection.close()
        return render_template(
            "shows/search-multiple-panelists.html", panelists=_panelists, shows=None
        )

    # Fallback for GET request
    _database_connection.close()
    return render_template(
        "shows/search-multiple-panelists.html", panelists=_panelists, shows=None
    )
