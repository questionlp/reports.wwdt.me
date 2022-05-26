# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Panelist vs Panelist Report Functions"""
from typing import Any, Dict

import mysql.connector


def retrieve_panelists(
    database_connection: mysql.connector.connect,
) -> Dict[str, Any]:
    """Retrieve panelists from the Stats Page database"""

    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT DISTINCT p.panelistid, p.panelist, p.panelistslug "
        "FROM ww_showpnlmap pm "
        "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
        "WHERE pm.panelistscore IS NOT NULL "
        "AND p.panelist <> '<Multiple>' "
        "ORDER BY p.panelist ASC;"
    )
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    panelists = {}
    for row in result:
        panelists[row.panelistslug] = {
            "id": row.panelistid,
            "name": row.panelist,
            "slug": row.panelistslug,
        }

    return panelists


def retrieve_panelist_appearances(
    panelists: Dict[str, Any], database_connection: mysql.connector.connect
) -> Dict[str, str]:
    """Retrieve panelist appearances from the Stats Page database"""

    if not database_connection.is_connected():
        database_connection.reconnect()

    panelist_appearances = {}
    for _, panelist_info in panelists.items():
        cursor = database_connection.cursor(named_tuple=True)
        query = (
            "SELECT s.showdate FROM ww_showpnlmap pm "
            "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
            "JOIN ww_shows s ON s.showid = pm.showid "
            "WHERE p.panelistslug = %s "
            "AND pm.panelistscore IS NOT NULL "
            "AND s.bestof = 0 "
            "AND s.repeatshowid IS NULL "
            "ORDER BY s.showdate ASC;"
        )
        cursor.execute(query, (panelist_info["slug"],))
        result = cursor.fetchall()
        cursor.close()

        if result:
            panelist_appearances[panelist_info["slug"]] = [
                appearance[0].isoformat() for appearance in result
            ]

    return panelist_appearances


def retrieve_show_scores(
    database_connection: mysql.connector.connect,
) -> Dict[str, Any]:
    """Retrieve scores for each show and panelist from the Stats Page
    Database"""

    if not database_connection.is_connected():
        database_connection.reconnect()

    shows = {}
    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT s.showdate, p.panelistslug, pm.panelistscore "
        "FROM ww_showpnlmap pm "
        "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
        "JOIN ww_shows s ON s.showid = pm.showid "
        "WHERE s.bestof = 0 "
        "AND s.repeatshowid IS NULL "
        "AND pm.panelistscore IS NOT NULL "
        "ORDER BY s.showdate ASC, pm.panelistscore DESC;"
    )
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if result:
        for show in result:
            show_date = show.showdate.isoformat()
            if show_date not in shows:
                shows[show_date] = {}

            shows[show_date][show.panelistslug] = show.panelistscore

    return shows


def generate_panelist_vs_panelist_results(
    panelists: Dict[str, Any],
    panelist_appearances: Dict[str, Any],
    show_scores: Dict[str, Any],
) -> Dict[str, Any]:
    """Generate panelist vs panelist results"""

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
