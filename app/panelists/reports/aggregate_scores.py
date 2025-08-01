# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Panelist Aggregate Scores Report Functions."""

from decimal import Decimal
from typing import Any

import numpy
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection


def retrieve_all_scores(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[int | Decimal]:
    """Retrieve a list of all panelist scores from non-Best Of and non-Repeat shows."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT pm.panelistscore_decimal
        FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        WHERE s.bestof = 0 AND s.repeatshowid IS NULL
        AND pm.panelistscore_decimal IS NOT NULL
        ORDER BY pm.panelistscore_decimal ASC;
    """

    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    return [row["panelistscore_decimal"] for row in result]


def retrieve_score_spread(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict[str, int | Decimal]]:
    """Retrieve a list of grouped panelist scores from non-Best Of and non-Repeat shows."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT pm.panelistscore_decimal,
        COUNT(pm.panelistscore_decimal) AS count
        FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        WHERE pm.panelistscore_decimal IS NOT NULL
        AND s.bestof = 0 AND s.repeatshowid IS NULL
        GROUP BY pm.panelistscore_decimal
        ORDER BY pm.panelistscore_decimal ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    scores = []
    for row in result:
        scores.append(
            {
                "score": row["panelistscore_decimal"],
                "count": row["count"],
            }
        )

    return scores


def calculate_stats(scores: list[int]) -> dict[str, Any]:
    """Calculate stats for all of the panelist scores."""
    return {
        "count": len(scores),
        "minimum": Decimal(numpy.amin(scores)),
        "maximum": Decimal(numpy.amax(scores)),
        "mean": round(Decimal(numpy.mean(scores)), 5),
        "median": Decimal(numpy.median(scores)),
        "standard_deviation": round(Decimal(numpy.std(scores)), 5),
        "sum": Decimal(numpy.sum(scores)),
    }
