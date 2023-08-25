# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2023 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Panelist Aggregate Scores Report Functions"""
from decimal import Decimal
from typing import Any, Dict, List, Union
from flask import current_app

import mysql.connector
import numpy


def retrieve_all_scores(
    database_connection: mysql.connector.connect, use_decimal_scores: bool = False
) -> List[Union[int, Decimal]]:
    """Retrieve a list of all panelist scores from non-Best Of and
    non-Repeat shows"""
    if (
        use_decimal_scores
        and not current_app.config["app_settings"]["has_decimal_scores_column"]
    ):
        return None

    if not database_connection.is_connected():
        database_connection.reconnect()

    if use_decimal_scores:
        query = """
            SELECT pm.panelistscore_decimal AS score FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE s.bestof = 0 AND s.repeatshowid IS NULL
            AND pm.panelistscore_decimal IS NOT NULL
            ORDER BY pm.panelistscore_decimal ASC;
            """
    else:
        query = """
            SELECT pm.panelistscore AS score FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE s.bestof = 0 AND s.repeatshowid IS NULL
            AND pm.panelistscore IS NOT NULL
            ORDER BY pm.panelistscore ASC;
            """
    cursor = database_connection.cursor(named_tuple=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    return [row.score for row in result]


def retrieve_score_spread(
    database_connection: mysql.connector.connect, use_decimal_scores: bool = False
) -> List[Dict[str, Union[int, Decimal]]]:
    """Retrieve a list of grouped panelist scores from non-Best Of and
    non-Repeat shows"""
    if (
        use_decimal_scores
        and not current_app.config["app_settings"]["has_decimal_scores_column"]
    ):
        return None

    if not database_connection.is_connected():
        database_connection.reconnect()

    if use_decimal_scores:
        query = """
            SELECT pm.panelistscore_decimal AS score,
            COUNT(pm.panelistscore_decimal) AS count
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE pm.panelistscore_decimal IS NOT NULL
            AND s.bestof = 0 AND s.repeatshowid IS NULL
            GROUP BY pm.panelistscore_decimal
            ORDER BY pm.panelistscore_decimal ASC;
            """
    else:
        query = """
            SELECT pm.panelistscore AS score,
            COUNT(pm.panelistscore) AS count
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE pm.panelistscore IS NOT NULL
            AND s.bestof = 0 AND s.repeatshowid IS NULL
            GROUP BY pm.panelistscore
            ORDER BY pm.panelistscore ASC;
            """
    cursor = database_connection.cursor(named_tuple=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    scores = []
    for row in result:
        scores.append(
            {
                "score": row.score,
                "count": row.count,
            }
        )

    return scores


def calculate_stats(scores: List[int], decimal_scores: bool = False) -> Dict[str, Any]:
    """Calculate stats for all of the panelist scores"""

    if decimal_scores:
        return {
            "count": len(scores),
            "minimum": Decimal(numpy.amin(scores)),
            "maximum": Decimal(numpy.amax(scores)),
            "mean": round(Decimal(numpy.mean(scores)), 5),
            "median": Decimal(numpy.median(scores)),
            "standard_deviation": round(Decimal(numpy.std(scores)), 5),
            "sum": Decimal(numpy.sum(scores)),
        }
    else:
        return {
            "count": len(scores),
            "minimum": int(numpy.amin(scores)),
            "maximum": int(numpy.amax(scores)),
            "mean": round(numpy.mean(scores), 5),
            "median": int(numpy.median(scores)),
            "standard_deviation": round(numpy.std(scores), 5),
            "sum": int(numpy.sum(scores)),
        }
