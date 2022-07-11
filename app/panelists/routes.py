# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""Panelists Routes for Wait Wait Reports"""
from flask import Blueprint, current_app, render_template, request
import mysql.connector

from app.dicts import RANK_MAP
from .reports.common import retrieve_panelists
from .reports.aggregate_scores import (
    retrieve_all_scores,
    calculate_stats,
    retrieve_score_spread,
)
from .reports.appearances import retrieve_first_most_recent_appearances
from .reports.appearances_by_year import (
    retrieve_all_appearance_counts,
    retrieve_all_years,
)
from .reports.bluff_stats import retrieve_all_panelist_bluff_stats
from .reports.debut_by_year import retrieve_show_years, panelist_debuts_by_year
from .reports.gender_stats import retrieve_stats_by_year_gender
from .reports.panelist_vs_panelist import (
    retrieve_panelists as pvp_retrieve_panelists,
    retrieve_panelist_appearances as pvp_retrieve_appearances,
    retrieve_show_scores as pvp_retrieve_scores,
    generate_panelist_vs_panelist_results as pvp_generate_results,
)
from .reports.panelist_vs_panelist_scoring import (
    retrieve_common_shows,
    retrieve_panelists_scores,
)
from .reports.rankings_summary import (
    retrieve_all_panelist_rankings,
)
from .reports.single_appearance import retrieve_single_appearances
from .reports.stats_summary import (
    retrieve_all_panelists_stats as summary_retrieve_all_stats,
)
from .reports.streaks import (
    calculate_panelist_losing_streaks,
    calculate_panelist_win_streaks,
)

blueprint = Blueprint("panelists", __name__, template_folder="templates")


@blueprint.route("/")
def index():
    """View: Panelists Index"""
    return render_template("panelists/_index.html")


@blueprint.route("/aggregate-scores")
def aggregate_scores():
    """View: Panelists Aggregate Scores Report"""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _scores = retrieve_all_scores(database_connection=_database_connection)
    _stats = calculate_stats(_scores)
    _aggregate = retrieve_score_spread(database_connection=_database_connection)
    _database_connection.close()
    return render_template(
        "panelists/aggregate-scores.html", stats=_stats, aggregate=_aggregate
    )


@blueprint.route("/appearances-by-year")
def appearances_by_year():
    """View: Panelists Appearances by Year Report"""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _panelists = retrieve_all_appearance_counts(
        database_connection=_database_connection
    )
    _show_years = retrieve_all_years(database_connection=_database_connection)
    _database_connection.close()
    return render_template(
        "panelists/appearances-by-year.html",
        panelists=_panelists,
        show_years=_show_years,
    )


@blueprint.route("/bluff-stats")
def bluff_stats():
    """View: Panelists Bluff the Listener Statistics Report"""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _panelists = retrieve_all_panelist_bluff_stats(
        database_connection=_database_connection
    )
    _database_connection.close()
    return render_template("panelists/bluff-stats.html", panelists=_panelists)


@blueprint.route("/debut-by-year")
def debut_by_year():
    """View: Panelists Debut by Year Report"""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _years = retrieve_show_years(database_connection=_database_connection)
    _debuts = panelist_debuts_by_year(database_connection=_database_connection)
    _database_connection.close()
    return render_template("panelists/debut-by-year.html", years=_years, debuts=_debuts)


@blueprint.route("/first-most-recent-appearances")
def first_most_recent_appearances():
    """View: Panelists First and Most Recent Appearances Report"""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _panelists_appearances = retrieve_first_most_recent_appearances(
        database_connection=_database_connection
    )
    _database_connection.close()
    return render_template(
        "panelists/first-most-recent-appearances.html",
        panelists_appearances=_panelists_appearances,
    )


@blueprint.route("/gender-stats")
def gender_stats():
    """View: Panelists Statistics by Gender Report"""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _stats = retrieve_stats_by_year_gender(database_connection=_database_connection)
    _database_connection.close()
    return render_template("panelists/gender-stats.html", gender_stats=_stats)


@blueprint.route("/losing-streaks")
def losing_streaks():
    """View: Panelists Losing Streaks Report"""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _panelists = retrieve_panelists(database_connection=_database_connection)
    _streaks = calculate_panelist_losing_streaks(
        panelists=_panelists, database_connection=_database_connection
    )
    _database_connection.close()
    return render_template(
        "panelists/losing-streaks.html", rank_map=RANK_MAP, losing_streaks=_streaks
    )


@blueprint.route("/panelist-pvp", methods=["GET", "POST"])
def panelist_pvp():
    """View: Panelist vs Panelist Report"""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _panelists_list = pvp_retrieve_panelists(database_connection=_database_connection)

    _panelists_info = {
        _panelists_list[pnl]["slug"]: _panelists_list[pnl]["name"]
        for pnl in _panelists_list
    }

    if request.method == "POST":
        # Parse panelist dropdown selections
        panelist = "panelist" in request.form and request.form["panelist"]
        if panelist in _panelists_info.keys():
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
                "panelists/panelist-pvp.html",
                all_panelists=_panelists_list,
                panelist_info=panelist_info,
                results=_results[panelist],
            )
        else:
            # No valid panelist returned
            _database_connection.close()
            return render_template(
                "panelists/panelist-pvp.html",
                all_panelists=_panelists_list,
                results=None,
            )

    # Fallback for GET request
    _database_connection.close()
    return render_template("panelists/panelist-pvp.html", all_panelists=_panelists_list)


@blueprint.route("/panelist-pvp/all")
def panelist_pvp_all():
    """View: Panelist vs Panelist Report"""
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
        "panelists/panelist-pvp-all.html",
        panelists=_panelists,
        results=_results,
    )


@blueprint.route("/panelist-vs-panelist-scoring", methods=["GET", "POST"])
def panelist_pvp_scoring():
    """View: Panelist vs Panelist Scoring Report"""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _panelists = retrieve_panelists(database_connection=_database_connection)

    if request.method == "POST":
        # Parse panelist dropdown selections
        panelist_1 = "panelist_1" in request.form and request.form["panelist_1"]
        panelist_2 = "panelist_2" in request.form and request.form["panelist_2"]

        # Create a set of panelist values to de-duplicate values
        deduped_panelists = set([panelist_1, panelist_2])
        if "" in deduped_panelists:
            deduped_panelists.remove("")

        if None in deduped_panelists:
            deduped_panelists.remove(None)

        if len(deduped_panelists) > 0 and deduped_panelists <= _panelists.keys():
            # Revert set back to list
            panelist_values = list(deduped_panelists)
            if len(panelist_values) == 2:
                shows = retrieve_common_shows(
                    panelist_slug_1=panelist_values[0],
                    panelist_slug_2=panelist_values[1],
                    database_connection=_database_connection,
                )
                scores = retrieve_panelists_scores(
                    show_ids=shows,
                    panelist_slug_a=panelist_values[0],
                    panelist_slug_b=panelist_values[1],
                    database_connection=_database_connection,
                )
                _database_connection.close()

                return render_template(
                    "panelists/panelist-pvp-scoring.html",
                    panelists=_panelists,
                    valid_selections=True,
                    scores=scores,
                    rank_map=RANK_MAP,
                )

            # Fallback for invalid panelist selections
            _database_connection.close()
            return render_template(
                "panelists/panelist-pvp-scoring.html",
                panelists=_panelists,
                valid_selections=False,
                scores=None,
            )

    # Fallback for GET request
    _database_connection.close()
    return render_template(
        "panelists/panelist-pvp-scoring.html", panelists=_panelists, scores=None
    )


@blueprint.route("/rankings-summary")
def rankings_summary():
    """View: Panelists Rankings Summary Report"""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _panelists = retrieve_panelists(database_connection=_database_connection)
    _rankings = retrieve_all_panelist_rankings(database_connection=_database_connection)
    _database_connection.close()
    return render_template(
        "panelists/rankings-summary.html",
        panelists=_panelists,
        panelists_rankings=_rankings,
    )


@blueprint.route("/single-appearance")
def single_appearance():
    """View: Panelists Single Appearance Report"""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _panelists = retrieve_single_appearances(database_connection=_database_connection)
    _database_connection.close()
    return render_template(
        "panelists/single-appearance.html",
        rank_map=RANK_MAP,
        panelists_appearance=_panelists,
    )


@blueprint.route("/stats-summary")
def stats_summary():
    """View: Panelists Statistics Summary Report"""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _panelists = retrieve_panelists(database_connection=_database_connection)
    _stats = summary_retrieve_all_stats(database_connection=_database_connection)
    _database_connection.close()
    return render_template(
        "panelists/stats-summary.html", panelists=_panelists, panelists_stats=_stats
    )


@blueprint.route("/win-streaks")
def win_streaks():
    """View: Panelists Win Streaks Report"""
    _database_connection = mysql.connector.connect(**current_app.config["database"])
    _panelists = retrieve_panelists(database_connection=_database_connection)
    _streaks = calculate_panelist_win_streaks(
        panelists=_panelists, database_connection=_database_connection
    )
    _database_connection.close()
    return render_template(
        "panelists/win-streaks.html", rank_map=RANK_MAP, win_streaks=_streaks
    )
