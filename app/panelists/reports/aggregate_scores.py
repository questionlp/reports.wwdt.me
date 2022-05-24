# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Panelist Aggregate Scores Report Functions"""
from typing import Any, Dict, List

import mysql.connector
import numpy


def retrieve_all_scores(database_connection: mysql.connector.connect) -> List[int]:
    """Retrieve a list of all panelist scores from non-Best Of and
    non-Repeat shows"""

    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(dictionary=False)
    query = (
        "SELECT pm.panelistscore FROM ww_showpnlmap pm "
        "JOIN ww_shows s ON s.showid = pm.showid "
        "WHERE s.bestof = 0 AND s.repeatshowid IS NULL "
        "AND pm.panelistscore IS NOT NULL "
        "ORDER BY pm.panelistscore ASC;"
    )
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    return [row[0] for row in result]


def retrieve_score_spread(
    database_connection: mysql.connector.connect,
) -> List[Dict[str, int]]:
    """Retrieve a list of grouped panelist scores from non-Best Of and
    non-Repeat shows"""

    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(dictionary=False)
    query = (
        "SELECT pm.panelistscore, COUNT(pm.panelistscore) "
        "FROM ww_showpnlmap pm "
        "JOIN ww_shows s ON s.showid = pm.showid "
        "WHERE pm.panelistscore IS NOT NULL "
        "AND s.bestof = 0 AND s.repeatshowid IS NULL "
        "GROUP BY pm.panelistscore "
        "ORDER BY pm.panelistscore ASC;"
    )
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    scores = []
    for row in result:
        scores.append(
            {
                "score": row[0],
                "count": row[1],
            }
        )

    return scores


def calculate_stats(scores: List[int]) -> Dict[str, Any]:
    """Calculate stats for all of the panelist scores"""

    return {
        "count": len(scores),
        "minimum": int(numpy.amin(scores)),
        "maximum": int(numpy.amax(scores)),
        "mean": round(numpy.mean(scores), 4),
        "median": int(numpy.median(scores)),
        "standard_deviation": round(numpy.std(scores), 4),
        "sum": int(numpy.sum(scores)),
    }
