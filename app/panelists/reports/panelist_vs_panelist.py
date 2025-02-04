# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Panelist vs Panelist Report Functions."""

from typing import Any

from flask import current_app
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection


def retrieve_panelists(
    database_connection: MySQLConnection | PooledMySQLConnection,
    use_decimal_scores: bool = False,
) -> dict[str, Any]:
    """Retrieve panelists from the Stats Page database."""
    if (
        use_decimal_scores
        and not current_app.config["app_settings"]["has_decimal_scores_column"]
    ):
        return None

    if not database_connection.is_connected():
        database_connection.reconnect()

    if use_decimal_scores:
        query = """
            SELECT DISTINCT p.panelistid, p.panelist, p.panelistslug
            FROM ww_showpnlmap pm
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            WHERE pm.panelistscore_decimal IS NOT NULL
            AND p.panelist <> '<Multiple>'
            ORDER BY p.panelist ASC;
            """
    else:
        query = """
            SELECT DISTINCT p.panelistid, p.panelist, p.panelistslug
            FROM ww_showpnlmap pm
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            WHERE pm.panelistscore IS NOT NULL
            AND p.panelist <> '<Multiple>'
            ORDER BY p.panelist ASC;
            """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    panelists = {}
    for row in result:
        panelists[row["panelistslug"]] = {
            "id": row["panelistid"],
            "name": row["panelist"],
            "slug": row["panelistslug"],
        }

    return panelists


def retrieve_panelist_appearances(
    panelists: dict[str, Any],
    database_connection: MySQLConnection | PooledMySQLConnection,
    use_decimal_scores: bool = False,
) -> dict[str, str]:
    """Retrieve panelist appearances from the Stats Page database."""
    if (
        use_decimal_scores
        and not current_app.config["app_settings"]["has_decimal_scores_column"]
    ):
        return None

    if not database_connection.is_connected():
        database_connection.reconnect()

    panelist_appearances = {}
    for _, panelist_info in panelists.items():
        if use_decimal_scores:
            query = """
                SELECT s.showdate FROM ww_showpnlmap pm
                JOIN ww_panelists p ON p.panelistid = pm.panelistid
                JOIN ww_shows s ON s.showid = pm.showid
                WHERE p.panelistslug = %s
                AND pm.panelistscore_decimal IS NOT NULL
                AND s.bestof = 0
                AND s.repeatshowid IS NULL
                ORDER BY s.showdate ASC;
                """
        else:
            query = """
                SELECT s.showdate FROM ww_showpnlmap pm
                JOIN ww_panelists p ON p.panelistid = pm.panelistid
                JOIN ww_shows s ON s.showid = pm.showid
                WHERE p.panelistslug = %s
                AND pm.panelistscore IS NOT NULL
                AND s.bestof = 0
                AND s.repeatshowid IS NULL
                ORDER BY s.showdate ASC;
                """
        cursor = database_connection.cursor(dictionary=False)
        cursor.execute(query, (panelist_info["slug"],))
        result = cursor.fetchall()
        cursor.close()

        if result:
            panelist_appearances[panelist_info["slug"]] = [
                appearance[0].isoformat() for appearance in result
            ]

    return panelist_appearances


def retrieve_show_scores(
    database_connection: MySQLConnection | PooledMySQLConnection,
    use_decimal_scores: bool = False,
) -> dict[str, Any]:
    """Retrieve scores for each show and panelist from the Stats Page Database."""
    if (
        use_decimal_scores
        and not current_app.config["app_settings"]["has_decimal_scores_column"]
    ):
        return None

    if not database_connection.is_connected():
        database_connection.reconnect()

    shows = {}

    if use_decimal_scores:
        query = """
            SELECT s.showdate, p.panelistslug, pm.panelistscore_decimal AS score
            FROM ww_showpnlmap pm
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE s.bestof = 0
            AND s.repeatshowid IS NULL
            AND pm.panelistscore_decimal IS NOT NULL
            ORDER BY s.showdate ASC, pm.panelistscore_decimal DESC;
            """
    else:
        query = """
            SELECT s.showdate, p.panelistslug, pm.panelistscore AS score
            FROM ww_showpnlmap pm
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE s.bestof = 0
            AND s.repeatshowid IS NULL
            AND pm.panelistscore IS NOT NULL
            ORDER BY s.showdate ASC, pm.panelistscore DESC;
            """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if result:
        for show in result:
            show_date = show["showdate"].isoformat()
            if show_date not in shows:
                shows[show_date] = {}

            shows[show_date][show["panelistslug"]] = show["score"]

    return shows


def generate_panelist_vs_panelist_results(
    panelists: dict[str, Any],
    panelist_appearances: dict[str, Any],
    show_scores: dict[str, Any],
) -> dict[str, Any]:
    """Generate panelist vs panelist results."""
    pvp_results = {}
    for _, panelist_a in panelists.items():
        panelist_a = panelist_a["slug"]
        pvp_results[panelist_a] = {}
        for _, panelist_b in panelists.items():
            panelist_b = panelist_b["slug"]
            if panelist_a != panelist_b:
                panelist_a_appearances = panelist_appearances[panelist_a]
                panelist_b_appearances = panelist_appearances[panelist_b]
                a_b_intersect = list(
                    set(panelist_a_appearances) & set(panelist_b_appearances)
                )
                a_b_intersect.sort()

                pvp_results[panelist_a][panelist_b] = {}
                wins = 0
                draws = 0
                losses = 0
                for show in a_b_intersect:
                    panelist_a_score = show_scores[show][panelist_a]
                    panelist_b_score = show_scores[show][panelist_b]
                    if panelist_a_score > panelist_b_score:
                        wins = wins + 1
                    elif panelist_a_score == panelist_b_score:
                        draws = draws + 1
                    else:
                        losses = losses + 1

                pvp_results[panelist_a][panelist_b]["wins"] = wins
                pvp_results[panelist_a][panelist_b]["draws"] = draws
                pvp_results[panelist_a][panelist_b]["losses"] = losses
                pvp_results[panelist_a][panelist_b]["total"] = wins + draws + losses

    return pvp_results
