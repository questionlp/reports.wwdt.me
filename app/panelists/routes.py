# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Panelists Routes for Wait Wait Reports."""

import mysql.connector
from flask import Blueprint, current_app, render_template, request

from app.dicts import RANK_MAP

from .reports.aggregate_scores import (
    calculate_stats,
    retrieve_all_scores,
    retrieve_score_spread,
)
from .reports.appearances import retrieve_first_most_recent_appearances
from .reports.appearances_by_year import (
    retrieve_all_appearance_counts,
    retrieve_all_appearance_counts_by_year,
    retrieve_all_years,
)
from .reports.average_scores_by_year import (
    retrieve_all_panelists_yearly_average,
    retrieve_panelist_yearly_average,
)
from .reports.bluff_stats import (
    retrieve_all_panelist_bluff_stats,
    retrieve_all_panelist_bluff_stats_by_year,
    retrieve_most_chosen_by_year,
    retrieve_most_chosen_correct_by_year,
    retrieve_most_correct_by_year,
    retrieve_panelist_bluffs_by_year,
)
from .reports.common import retrieve_panelists
from .reports.debut_by_year import panelist_debuts_by_year, retrieve_show_years
from .reports.first_appearance_wins import retrieve_panelists_first_appearance_wins
from .reports.gender_stats import retrieve_stats_by_year_gender
from .reports.highest_scores_correct import (
    retrieve_highest_average_correct_answers_by_year,
    retrieve_highest_average_scores_by_year,
)
from .reports.panelist_vs_panelist import (
    generate_panelist_vs_panelist_results as pvp_generate_results,
)
from .reports.panelist_vs_panelist import (
    retrieve_panelist_appearances as pvp_retrieve_appearances,
)
from .reports.panelist_vs_panelist import retrieve_panelists as pvp_retrieve_panelists
from .reports.panelist_vs_panelist import retrieve_show_scores as pvp_retrieve_scores
from .reports.panelist_vs_panelist_scoring import (
    retrieve_common_shows,
    retrieve_panelists_scores,
)
from .reports.perfect_scores import retrieve_perfect_score_counts
from .reports.rankings_summary import retrieve_all_panelist_rankings
from .reports.show_appearances import retrieve_appearance_details
from .reports.single_appearance import retrieve_single_appearances
from .reports.stats_summary import (
    retrieve_all_panelists_stats as summary_retrieve_all_stats,
)
from .reports.stats_summary_by_year import retrieve_stats_all_years
from .reports.streaks import (
    calculate_panelist_losing_streaks,
    calculate_panelist_win_streaks,
)
from .reports.wins import retrieve_combined_outright_wins_ties_by_year

blueprint = Blueprint("panelists", __name__, template_folder="templates")


@blueprint.route("/")
def index() -> str:
    """View: Index."""
    return render_template("panelists/_index.html")


@blueprint.route("/aggregate-scores")
def aggregate_scores() -> str:
    """View: Aggregate Scores Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _scores = retrieve_all_scores(
        database_connection=_database_connection,
        use_decimal_scores=current_app.config["app_settings"]["use_decimal_scores"],
    )
    _stats = calculate_stats(
        _scores,
        decimal_scores=current_app.config["app_settings"]["use_decimal_scores"],
    )
    _aggregate = retrieve_score_spread(
        database_connection=_database_connection,
        use_decimal_scores=current_app.config["app_settings"]["use_decimal_scores"],
    )
    _database_connection.close()
    return render_template(
        "panelists/aggregate-scores.html", stats=_stats, aggregate=_aggregate
    )


@blueprint.route("/appearances-by-year", methods=["GET", "POST"])
def appearances_by_year() -> str:
    """View: Appearances by Year Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _panelists = retrieve_panelists(database_connection=_database_connection)
    _panelists_dict = {panelist["slug"]: panelist["name"] for panelist in _panelists}
    _show_years = retrieve_show_years(database_connection=_database_connection)

    if request.method == "POST":
        # Parse panelist dropdown selections
        _panelist = "panelist" in request.form and request.form["panelist"]

        if _panelist in _panelists_dict:
            _panelist_info = {"slug": _panelist, "name": _panelists_dict[_panelist]}
            _appearances = retrieve_appearance_details(
                panelist_slug=_panelist,
                database_connection=_database_connection,
                include_decimal_scores=current_app.config["app_settings"][
                    "use_decimal_scores"
                ],
            )
            _database_connection.close()
            return render_template(
                "panelists/appearances-by-year.html",
                panelists=_panelists,
                years=_show_years,
                panelist_info=_panelist_info,
                appearances=_appearances,
                rank_map=RANK_MAP,
            )

        # No valid panelist returned
        _database_connection.close()
        return render_template(
            "panelists/appearances-by-year.html",
            panelists=_panelists,
            years=_show_years,
            appearances=None,
        )

    # Fallback for GET request
    _database_connection.close()
    return render_template(
        "panelists/appearances-by-year.html", panelists=_panelists, years=_show_years
    )


@blueprint.route("/appearance-counts-by-year")
def appearance_counts_by_year() -> str:
    """View: Appearance Counts by Year Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _appearances = retrieve_all_appearance_counts_by_year(
        database_connection=_database_connection
    )
    _database_connection.close()

    return render_template(
        "panelists/appearance-counts-by-year.html",
        years=list(_appearances.keys()),
        appearances=_appearances,
    )


@blueprint.route("/appearance-counts-by-year/grid")
def appearance_counts_by_year_grid() -> str:
    """View: Appearance Counts by Year Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _panelists = retrieve_all_appearance_counts(
        database_connection=_database_connection
    )
    _show_years = retrieve_all_years(database_connection=_database_connection)
    _database_connection.close()
    return render_template(
        "panelists/appearance-counts-by-year-grid.html",
        panelists=_panelists,
        show_years=_show_years,
    )


@blueprint.route("/average-scores-by-year", methods=["GET", "POST"])
def average_scores_by_year() -> str:
    """View: Average Scores by Year Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _panelists_list = pvp_retrieve_panelists(database_connection=_database_connection)

    _panelists_info = {
        _panelists_list[pnl]["slug"]: _panelists_list[pnl]["name"]
        for pnl in _panelists_list
    }

    if request.method == "POST":
        # Parse panelist dropdown selections
        panelist = "panelist" in request.form and request.form["panelist"]
        if panelist in _panelists_info:
            # Retrieve average scores for the panelist
            panelist_info = {"slug": panelist, "name": _panelists_info[panelist]}
            average_scores = retrieve_panelist_yearly_average(
                panelist_slug=panelist,
                database_connection=_database_connection,
                use_decimal_scores=current_app.config["app_settings"][
                    "use_decimal_scores"
                ],
            )
            _database_connection.close()
            return render_template(
                "panelists/average-scores-by-year.html",
                all_panelists=_panelists_list,
                panelist_info=panelist_info,
                average_scores=average_scores,
            )

        # No valid panelist returned
        _database_connection.close()
        return render_template(
            "panelists/average-scores-by-year.html",
            all_panelists=_panelists_list,
            average_scores=None,
        )

    # Fallback for GET request
    _database_connection.close()
    return render_template(
        "panelists/average-scores-by-year.html", all_panelists=_panelists_list
    )


@blueprint.route("/average-scores-by-year-all")
def average_scores_by_year_all() -> str:
    """View: Average Scores by Year: All Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    average_scores = retrieve_all_panelists_yearly_average(
        database_connection=_database_connection,
        use_decimal_scores=current_app.config["app_settings"]["use_decimal_scores"],
    )
    years = retrieve_all_years(database_connection=_database_connection)
    if average_scores and years:
        return render_template(
            "panelists/average-scores-by-year-all.html",
            average_scores=average_scores,
            years=years,
        )

    return render_template("panelists/average-scores-by-year-all.html")


@blueprint.route("/bluff-the-listener-statistics")
def bluff_the_listener_statistics() -> str:
    """View: Bluff the Listener Statistics Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _panelists = retrieve_all_panelist_bluff_stats(
        database_connection=_database_connection
    )
    _database_connection.close()
    return render_template(
        "panelists/bluff-the-listener-statistics.html", panelists=_panelists
    )


@blueprint.route("/bluff-the-listener-statistics-by-year", methods=["GET", "POST"])
def bluff_the_listener_statistics_by_year() -> str:
    """View: Bluff the Listener Statistics by Year Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _show_years = retrieve_show_years(database_connection=_database_connection)
    if request.method == "POST":
        # Parse panelist dropdown selections
        _year = "year" in request.form and request.form["year"]
        try:
            year = int(_year)
        except ValueError:
            year = None

        if year not in _show_years:
            _database_connection.close()
            return render_template(
                "panelists/bluff-the-listener-statistics-by-year.html",
                show_years=_show_years,
                bluff_stats=None,
            )

        _bluff_stats = retrieve_all_panelist_bluff_stats_by_year(
            year=year, database_connection=_database_connection
        )
        if not _bluff_stats:
            _database_connection.close()
            return render_template(
                "panelists/bluff-the-listener-statistics-by-year.html",
                show_years=_show_years,
                bluff_stats=None,
            )

        _database_connection.close()
        return render_template(
            "panelists/bluff-the-listener-statistics-by-year.html",
            show_years=_show_years,
            year=year,
            bluff_stats=_bluff_stats,
        )

    # Fallback for GET request
    _database_connection.close()
    return render_template(
        "panelists/bluff-the-listener-statistics-by-year.html",
        show_years=_show_years,
        bluff_stats=None,
    )


@blueprint.route(
    "/bluff-the-listener-panelist-statistics-by-year", methods=["GET", "POST"]
)
def bluff_the_listener_panelist_statistics_by_year() -> str:
    """View: Bluff the Listener Panelist Statistics by Year Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _panelists = retrieve_panelists(database_connection=_database_connection)
    _panelists_dict = {panelist["slug"]: panelist["name"] for panelist in _panelists}

    if request.method == "POST":
        # Parse panelist dropdown selections
        panelist = "panelist" in request.form and request.form["panelist"]

        if panelist not in _panelists_dict:
            _database_connection.close()
            return render_template(
                "panelists/bluff-the-listener-panelist-statistics-by-year.html",
                panelists=_panelists_dict,
                bluff_stats=None,
            )

        _bluff_stats = retrieve_panelist_bluffs_by_year(
            panelist_slug=panelist, database_connection=_database_connection
        )
        if not _bluff_stats:
            _database_connection.close()
            return render_template(
                "panelists/bluff-the-listener-panelist-statistics-by-year.html",
                panelists=_panelists_dict,
                bluff_stats=None,
            )

        _database_connection.close()
        return render_template(
            "panelists/bluff-the-listener-panelist-statistics-by-year.html",
            panelists=_panelists_dict,
            bluff_stats=_bluff_stats,
        )

    # Fallback for GET request
    _database_connection.close()
    return render_template(
        "panelists/bluff-the-listener-panelist-statistics-by-year.html",
        panelists=_panelists_dict,
        bluff_stats=None,
    )


@blueprint.route("/debuts-by-year")
def debuts_by_year() -> str:
    """View: Debuts by Year Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _years = retrieve_show_years(database_connection=_database_connection)
    _debuts = panelist_debuts_by_year(database_connection=_database_connection)
    _database_connection.close()
    return render_template(
        "panelists/debuts-by-year.html", years=_years, debuts=_debuts
    )


@blueprint.route("/first-appearance-wins")
def first_appearance_wins() -> str:
    """View: First Appearance Wins Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _panelists = retrieve_panelists_first_appearance_wins(
        database_connection=_database_connection,
        use_decimal_scores=current_app.config["app_settings"]["use_decimal_scores"],
    )
    _database_connection.close()
    return render_template(
        "panelists/first-appearance-wins.html", panelists=_panelists, rank_map=RANK_MAP
    )


@blueprint.route("/first-most-recent-appearances")
def first_most_recent_appearances() -> str:
    """View: First and Most Recent Appearances Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _panelists_appearances = retrieve_first_most_recent_appearances(
        database_connection=_database_connection
    )
    _database_connection.close()
    return render_template(
        "panelists/first-most-recent-appearances.html",
        panelists_appearances=_panelists_appearances,
    )


@blueprint.route("/highest-average-correct-answers-by-year", methods=["GET", "POST"])
def highest_average_correct_answers_by_year() -> str:
    """View: Highest Average Correct Answers by Year Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _show_years = retrieve_show_years(database_connection=_database_connection)

    if request.method == "POST":
        # Parse panelist dropdown selections
        _year = "year" in request.form and request.form["year"]
        _exclude_single = (
            "exclude_single" in request.form and request.form["exclude_single"] == "on"
        )
        try:
            year = int(_year)
        except ValueError:
            year = None

        if year not in _show_years:
            _database_connection.close()
            return render_template(
                "panelists/highest-average-correct-answers-by-year.html",
                show_years=_show_years,
                win_stats=None,
            )

        _score_stats = retrieve_highest_average_correct_answers_by_year(
            year=year,
            database_connection=_database_connection,
            use_decimal_scores=current_app.config["app_settings"]["use_decimal_scores"],
            exclude_single_appearances=_exclude_single,
        )
        if not _score_stats:
            _database_connection.close()
            return render_template(
                "panelists/highest-average-correct-answers-by-year.html",
                show_years=_show_years,
                score_stats=None,
            )

        _database_connection.close()
        return render_template(
            "panelists/highest-average-correct-answers-by-year.html",
            show_years=_show_years,
            year=year,
            score_stats=_score_stats,
        )

    # Fallback for GET request
    _database_connection.close()
    return render_template(
        "panelists/highest-average-correct-answers-by-year.html",
        show_years=_show_years,
        score_stats=None,
    )


@blueprint.route("/highest-average-scores-by-year", methods=["GET", "POST"])
def highest_average_scores_by_year() -> str:
    """View: Highest Average Scores by Year Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _show_years = retrieve_show_years(database_connection=_database_connection)

    if request.method == "POST":
        # Parse panelist dropdown selections
        _year = "year" in request.form and request.form["year"]
        _exclude_single = (
            "exclude_single" in request.form and request.form["exclude_single"] == "on"
        )
        try:
            year = int(_year)
        except ValueError:
            year = None

        if year not in _show_years:
            _database_connection.close()
            return render_template(
                "panelists/highest-average-scores-by-year.html",
                show_years=_show_years,
                win_stats=None,
            )

        _score_stats = retrieve_highest_average_scores_by_year(
            year=year,
            database_connection=_database_connection,
            use_decimal_scores=current_app.config["app_settings"]["use_decimal_scores"],
            exclude_single_appearances=_exclude_single,
        )
        if not _score_stats:
            _database_connection.close()
            return render_template(
                "panelists/highest-average-scores-by-year.html",
                show_years=_show_years,
                score_stats=None,
            )

        _database_connection.close()
        return render_template(
            "panelists/highest-average-scores-by-year.html",
            show_years=_show_years,
            year=year,
            score_stats=_score_stats,
        )

    # Fallback for GET request
    _database_connection.close()
    return render_template(
        "panelists/highest-average-scores-by-year.html",
        show_years=_show_years,
        score_stats=None,
    )


@blueprint.route("/losing-streaks")
def losing_streaks() -> str:
    """View: Losing Streaks Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _panelists = retrieve_panelists(database_connection=_database_connection)
    _streaks = calculate_panelist_losing_streaks(
        panelists=_panelists, database_connection=_database_connection
    )
    _database_connection.close()
    return render_template("panelists/losing-streaks.html", losing_streaks=_streaks)


@blueprint.route("/most-chosen-bluff-the-listener-by-year", methods=["GET", "POST"])
def most_chosen_bluff_the_listener_by_year() -> str:
    """View: Most Chosen Bluff the Listener Story by Year Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _show_years = retrieve_show_years(database_connection=_database_connection)

    if request.method == "POST":
        # Parse panelist dropdown selections
        _year = "year" in request.form and request.form["year"]
        try:
            year = int(_year)
        except ValueError:
            year = None

        if year not in _show_years:
            _database_connection.close()
            return render_template(
                "panelists/most-chosen-bluff-the-listener-by-year.html",
                show_years=_show_years,
                bluff_stats=None,
            )

        _bluff_stats = retrieve_most_chosen_by_year(
            year=year, database_connection=_database_connection
        )
        if not _bluff_stats:
            _database_connection.close()
            return render_template(
                "panelists/most-chosen-bluff-the-listener-by-year.html",
                show_years=_show_years,
                bluff_stats=None,
            )

        _database_connection.close()
        return render_template(
            "panelists/most-chosen-bluff-the-listener-by-year.html",
            show_years=_show_years,
            year=year,
            bluff_stats=_bluff_stats,
        )

    # Fallback for GET request
    _database_connection.close()
    return render_template(
        "panelists/most-chosen-bluff-the-listener-by-year.html",
        show_years=_show_years,
        bluff_stats=None,
    )


@blueprint.route(
    "/most-chosen-correct-bluff-the-listener-by-year", methods=["GET", "POST"]
)
def most_chosen_correct_bluff_the_listener_by_year() -> str:
    """View: Most Chosen Correct Bluff the Listener Story by Year Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _show_years = retrieve_show_years(database_connection=_database_connection)

    if request.method == "POST":
        # Parse panelist dropdown selections
        _year = "year" in request.form and request.form["year"]
        try:
            year = int(_year)
        except ValueError:
            year = None

        if year not in _show_years:
            _database_connection.close()
            return render_template(
                "panelists/most-chosen-correct-bluff-the-listener-by-year.html",
                show_years=_show_years,
                bluff_stats=None,
            )

        _bluff_stats = retrieve_most_chosen_correct_by_year(
            year=year, database_connection=_database_connection
        )
        if not _bluff_stats:
            _database_connection.close()
            return render_template(
                "panelists/most-chosen-correct-bluff-the-listener-by-year.html",
                show_years=_show_years,
                bluff_stats=None,
            )

        _database_connection.close()
        return render_template(
            "panelists/most-chosen-correct-bluff-the-listener-by-year.html",
            show_years=_show_years,
            year=year,
            bluff_stats=_bluff_stats,
        )

    # Fallback for GET request
    _database_connection.close()
    return render_template(
        "panelists/most-chosen-correct-bluff-the-listener-by-year.html",
        show_years=_show_years,
        bluff_stats=None,
    )


@blueprint.route("/most-correct-bluff-the-listener-by-year", methods=["GET", "POST"])
def most_correct_bluff_the_listener_by_year() -> str:
    """View: Most Correct Bluff the Listener Story by Year Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _show_years = retrieve_show_years(database_connection=_database_connection)

    if request.method == "POST":
        # Parse panelist dropdown selections
        _year = "year" in request.form and request.form["year"]
        try:
            year = int(_year)
        except ValueError:
            year = None

        if year not in _show_years:
            _database_connection.close()
            return render_template(
                "panelists/most-correct-bluff-the-listener-by-year.html",
                show_years=_show_years,
                bluff_stats=None,
            )

        _bluff_stats = retrieve_most_correct_by_year(
            year=year, database_connection=_database_connection
        )
        if not _bluff_stats:
            _database_connection.close()
            return render_template(
                "panelists/most-correct-bluff-the-listener-by-year.html",
                show_years=_show_years,
                bluff_stats=None,
            )

        _database_connection.close()
        return render_template(
            "panelists/most-correct-bluff-the-listener-by-year.html",
            show_years=_show_years,
            year=year,
            bluff_stats=_bluff_stats,
        )

    # Fallback for GET request
    _database_connection.close()
    return render_template(
        "panelists/most-correct-bluff-the-listener-by-year.html",
        show_years=_show_years,
        bluff_stats=None,
    )


@blueprint.route("/most-wins-by-year", methods=["GET", "POST"])
def most_wins_by_year() -> str:
    """View: Most Wins by Year Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _show_years = retrieve_show_years(database_connection=_database_connection)

    if request.method == "POST":
        # Parse panelist dropdown selections
        _year = "year" in request.form and request.form["year"]
        try:
            year = int(_year)
        except ValueError:
            year = None

        if year not in _show_years:
            _database_connection.close()
            return render_template(
                "panelists/most-wins-by-year.html",
                show_years=_show_years,
                win_stats=None,
            )

        _win_stats = retrieve_combined_outright_wins_ties_by_year(
            year=year, database_connection=_database_connection
        )
        if not _win_stats:
            _database_connection.close()
            return render_template(
                "panelists/most-wins-by-year.html",
                show_years=_show_years,
                win_stats=None,
            )

        _database_connection.close()
        return render_template(
            "panelists/most-wins-by-year.html",
            show_years=_show_years,
            year=year,
            win_stats=_win_stats,
        )

    # Fallback for GET request
    _database_connection.close()
    return render_template(
        "panelists/most-wins-by-year.html",
        show_years=_show_years,
        win_stats=None,
    )


@blueprint.route("/panelist-vs-panelist", methods=["GET", "POST"])
def panelist_vs_panelist() -> str:
    """View: Panelist vs Panelist Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _panelists_list = pvp_retrieve_panelists(database_connection=_database_connection)

    _panelists_info = {
        _panelists_list[pnl]["slug"]: _panelists_list[pnl]["name"]
        for pnl in _panelists_list
    }

    if request.method == "POST":
        # Parse panelist dropdown selections
        panelist = "panelist" in request.form and request.form["panelist"]
        if panelist in _panelists_info:
            # Retrieve PvP report for specific panelist
            panelist_info = {"slug": panelist, "name": _panelists_info[panelist]}
            _appearances = pvp_retrieve_appearances(
                panelists=_panelists_list, database_connection=_database_connection
            )
            _scores = pvp_retrieve_scores(database_connection=_database_connection)
            _results = pvp_generate_results(
                panelists=_panelists_list,
                panelist_appearances=_appearances,
                show_scores=_scores,
            )
            _database_connection.close()
            return render_template(
                "panelists/panelist-vs-panelist.html",
                all_panelists=_panelists_list,
                panelist_info=panelist_info,
                results=_results[panelist],
            )

        # No valid panelist returned
        _database_connection.close()
        return render_template(
            "panelists/panelist-vs-panelist.html",
            all_panelists=_panelists_list,
            results=None,
        )

    # Fallback for GET request
    _database_connection.close()
    return render_template(
        "panelists/panelist-vs-panelist.html", all_panelists=_panelists_list
    )


@blueprint.route("/panelist-vs-panelist/all")
def panelist_vs_panelist_all() -> str:
    """View: Panelist vs Panelist: All Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _panelists = pvp_retrieve_panelists(database_connection=_database_connection)
    _appearances = pvp_retrieve_appearances(
        panelists=_panelists, database_connection=_database_connection
    )
    _scores = pvp_retrieve_scores(database_connection=_database_connection)
    _results = pvp_generate_results(
        panelists=_panelists,
        panelist_appearances=_appearances,
        show_scores=_scores,
    )
    _database_connection.close()

    return render_template(
        "panelists/panelist-vs-panelist-all.html",
        panelists=_panelists,
        results=_results,
    )


@blueprint.route("/panelist-vs-panelist-scoring", methods=["GET", "POST"])
def panelist_vs_panelist_scoring() -> str:
    """View: Panelist vs Panelist Scoring Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _panelists = retrieve_panelists(database_connection=_database_connection)
    _panelists_dict = {panelist["slug"]: panelist["name"] for panelist in _panelists}

    if request.method == "POST":
        # Parse panelist dropdown selections
        panelist_1 = "panelist_1" in request.form and request.form["panelist_1"]
        panelist_2 = "panelist_2" in request.form and request.form["panelist_2"]

        # Create a set of panelist values to de-duplicate values
        # deduped_panelists = set([panelist_1, panelist_2])
        deduped_panelists = {panelist_1, panelist_2}
        if "" in deduped_panelists:
            deduped_panelists.remove("")

        if None in deduped_panelists:
            deduped_panelists.remove(None)

        if len(deduped_panelists) > 0 and deduped_panelists <= _panelists_dict.keys():
            # Revert set back to list
            panelist_values = list(deduped_panelists)
            if len(panelist_values) == 2:
                shows = retrieve_common_shows(
                    panelist_slug_1=panelist_values[0],
                    panelist_slug_2=panelist_values[1],
                    database_connection=_database_connection,
                    use_decimal_scores=current_app.config["app_settings"][
                        "use_decimal_scores"
                    ],
                )
                scores = retrieve_panelists_scores(
                    show_ids=shows,
                    panelist_slug_a=panelist_values[0],
                    panelist_slug_b=panelist_values[1],
                    database_connection=_database_connection,
                    use_decimal_scores=current_app.config["app_settings"][
                        "use_decimal_scores"
                    ],
                )
                _database_connection.close()

                return render_template(
                    "panelists/panelist-vs-panelist-scoring.html",
                    panelists=_panelists_dict,
                    valid_selections=True,
                    scores=scores,
                )

            # Fallback for invalid panelist selections
            _database_connection.close()
            return render_template(
                "panelists/panelist-vs-panelist-scoring.html",
                panelists=_panelists_dict,
                valid_selections=False,
                scores=None,
            )

    # Fallback for GET request
    _database_connection.close()
    return render_template(
        "panelists/panelist-vs-panelist-scoring.html",
        panelists=_panelists_dict,
        scores=None,
    )


@blueprint.route("/perfect-score-counts")
def perfect_score_counts() -> str:
    """View: Perfect Score Counts Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _counts = retrieve_perfect_score_counts(
        database_connection=_database_connection,
        use_decimal_scores=current_app.config["app_settings"]["use_decimal_scores"],
    )
    _database_connection.close()
    return render_template("panelists/perfect-score-counts.html", counts=_counts)


@blueprint.route("/rankings-summary")
def rankings_summary() -> str:
    """View: Rankings Summary Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _panelists = retrieve_panelists(database_connection=_database_connection)
    _panelists_dict = {panelist["slug"]: panelist["name"] for panelist in _panelists}
    _rankings = retrieve_all_panelist_rankings(database_connection=_database_connection)
    _database_connection.close()
    return render_template(
        "panelists/rankings-summary.html",
        panelists=_panelists_dict,
        panelists_rankings=_rankings,
    )


@blueprint.route("/single-appearance")
def single_appearance() -> str:
    """View: Single Appearance Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _panelists = retrieve_single_appearances(
        database_connection=_database_connection,
        use_decimal_scores=current_app.config["app_settings"]["use_decimal_scores"],
    )
    _database_connection.close()
    return render_template(
        "panelists/single-appearance.html",
        panelists_appearance=_panelists,
    )


@blueprint.route("/statistics-by-gender")
def statistics_by_gender() -> str:
    """View: Statistics by Gender Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _stats = retrieve_stats_by_year_gender(
        database_connection=_database_connection,
        use_decimal_scores=current_app.config["app_settings"]["use_decimal_scores"],
    )
    _database_connection.close()
    return render_template("panelists/statistics-by-gender.html", gender_stats=_stats)


@blueprint.route("/statistics-summary")
def statistics_summary() -> str:
    """View: Statistics Summary Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _panelists = retrieve_panelists(database_connection=_database_connection)
    _panelists_dict = {panelist["slug"]: panelist["name"] for panelist in _panelists}
    _stats = summary_retrieve_all_stats(
        database_connection=_database_connection,
        use_decimal_scores=current_app.config["app_settings"]["use_decimal_scores"],
    )
    _database_connection.close()
    return render_template(
        "panelists/statistics-summary.html",
        panelists=_panelists_dict,
        panelists_stats=_stats,
    )


@blueprint.route("/statistics-summary-by-year", methods=["GET", "POST"])
def statistics_summary_by_year() -> str:
    """View: Statistics Summary by Year Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _panelists = retrieve_panelists(database_connection=_database_connection)
    _panelists_dict = {panelist["slug"]: panelist["name"] for panelist in _panelists}

    if request.method == "POST":
        # Parse panelist dropdown selections
        panelist = "panelist" in request.form and request.form["panelist"]

        if panelist not in _panelists_dict:
            _database_connection.close()
            return render_template(
                "panelists/statistics-summary-by-year.html",
                panelists=_panelists_dict,
                bluff_stats=None,
            )

        _stats = retrieve_stats_all_years(
            panelist_slug=panelist,
            database_connection=_database_connection,
            use_decimal_scores=current_app.config["app_settings"]["use_decimal_scores"],
        )

        if not _stats:
            _database_connection.close()
            return render_template(
                "panelists/statistics-summary-by-year.html",
                panelists=_panelists_dict,
                panelist_stats=None,
            )

        _database_connection.close()
        return render_template(
            "panelists/statistics-summary-by-year.html",
            panelists=_panelists_dict,
            panelist_stats=_stats,
            # use_decimal_scores=current_app.config["app_settings"]["use_decimal_scores"],
        )

    # Fallback for GET request
    _database_connection.close()
    return render_template(
        "panelists/statistics-summary-by-year.html",
        panelists=_panelists_dict,
        panelist_stats=None,
    )


@blueprint.route("/win-streaks")
def win_streaks() -> str:
    """View: Win Streaks Report."""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _panelists = retrieve_panelists(database_connection=_database_connection)
    _streaks = calculate_panelist_win_streaks(
        panelists=_panelists, database_connection=_database_connection
    )
    _database_connection.close()
    return render_template("panelists/win-streaks.html", win_streaks=_streaks)
