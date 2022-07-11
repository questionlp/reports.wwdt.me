# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Panelist vs Panelist Scoring Report Functions"""
from typing import Any, Dict, List

import mysql.connector


def retrieve_common_shows(
    panelist_slug_1: str,
    panelist_slug_2: str,
    database_connection: mysql.connector.connect,
) -> List[int]:
    """Retrieve shows in which the two panelists have appeared
    together on a panel, excluding Best Of, Repeats and the 20th
    Anniversary special"""

    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT pm.showid FROM ww_showpnlmap pm "
        "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
        "JOIN ww_shows s ON s.showid = pm.showid "
        "WHERE p.panelistslug IN (%s, %s) "
        "AND s.showdate <> '2018-10-27' "
        "AND s.bestof = 0 AND s.repeatshowid IS NULL "
        "AND pm.panelistscore IS NOT NULL "
        "GROUP BY pm.showid "
        "HAVING COUNT(pm.showid) = 2 "
        "ORDER BY s.showdate ASC;"
    )
    cursor.execute(
        query,
        (
            panelist_slug_1,
            panelist_slug_2,
        ),
    )
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    return [row.showid for row in result]


def retrieve_panelists_scores(
    show_ids: List[int],
    panelist_slug_a: str,
    panelist_slug_b: str,
    database_connection: mysql.connector.connect,
) -> Dict[str, Any]:
    """Retrieves panelists scores for the two requested panelists"""

    if not show_ids:
        return None

    if not database_connection.is_connected():
        database_connection.reconnect()

    show_scores = {}
    for show_id in show_ids:
        cursor = database_connection.cursor(named_tuple=True)

        query = (
            "SELECT s.showdate, p.panelist, p.panelistslug, "
            "pm.panelistscore, pm.showpnlrank FROM ww_showpnlmap pm "
            "JOIN ww_shows s ON s.showid = pm.showid "
            "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
            "WHERE s.showid = %s "
            "AND p.panelistslug IN (%s, %s);"
        )
        cursor.execute(
            query,
            (
                show_id,
                panelist_slug_a,
                panelist_slug_b,
            ),
        )
        result = cursor.fetchall()

        if not result:
            return None

        for row in result:
            show_date = row.showdate.isoformat()
            if show_date not in show_scores:
                show_scores[show_date] = {}

            panelist_info = {
                "slug": row.panelistslug,
                "name": row.panelist,
                "score": row.panelistscore,
                "rank": row.showpnlrank,
            }
            show_scores[show_date][row.panelistslug] = panelist_info

    return show_scores
