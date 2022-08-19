# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Panelist Perfect Scores Report Functions"""
from typing import Dict, Union

import mysql.connector


def retrieve_perfect_score_counts(
    database_connection: mysql.connector.connect,
) -> Dict[str, Union[str, int]]:
    """Returns a dictionary containing counts of how many times
    panelists have scored a "perfect" score (20 points or higher).
    Excludes Best Of and repeat shows."""

    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT p.panelist, ANY_VALUE(p.panelistslug) AS panelistslug, "
        "COUNT(p.panelist) AS count "
        "FROM ww_showpnlmap pm "
        "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
        "JOIN ww_shows s ON s.showid = pm.showid "
        "WHERE pm.panelistscore >= 20 "
        "AND s.bestof = 0 AND s.repeatshowid IS NULL "
        "GROUP BY p.panelist "
        "ORDER BY COUNT(p.panelist) DESC;"
    )
    cursor.execute(query)
    results = cursor.fetchall()

    if not results:
        return None

    panelists = {}
    for row in results:
        panelists[row.panelistslug] = {
            "name": row.panelist,
            "slug": row.panelistslug,
            "more_perfect": row.count,
        }

    query = (
        "SELECT p.panelist, ANY_VALUE(p.panelistslug) AS panelistslug, "
        "COUNT(p.panelist) AS count "
        "FROM ww_showpnlmap pm "
        "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
        "JOIN ww_shows s ON s.showid = pm.showid "
        "WHERE pm.panelistscore = 20 "
        "AND s.bestof = 0 AND s.repeatshowid IS NULL "
        "GROUP BY p.panelist;"
    )
    cursor.execute(query)
    results = cursor.fetchall()

    if not results:
        return None

    for row in results:
        panelists[row.panelistslug]["perfect"] = row.count

    return panelists
