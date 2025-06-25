# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Location Score Breakdown Report Functions."""

from decimal import Decimal
from typing import Any

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection


def retrieve_average_scores_by_location(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict[str, Any]]:
    """Retrieve average scores sorted by location."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    # Excluding 25th Anniversary Show at Chicago Theatre from calculations
    # due to non-standard number of panelist scores and score totals
    query = """
        SELECT l.locationid, l.locationslug, l.venue, l.city, l.state,
        AVG(pm.panelistscore_decimal) AS average_score,
        SUM(pm.panelistscore_decimal) / (COUNT(s.showid) / 3) AS average_total,
        COUNT(s.showid) / 3 AS show_count
        FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        JOIN ww_showlocationmap lm ON lm.showid = pm.showid
        JOIN ww_locations l ON l.locationid = lm.locationid
        WHERE s.bestof = 0 AND s.repeatshowid IS NULL
        AND l.locationid <> 3 -- Ignore any TBD locations
        AND s.showdate <> '2018-10-27'
        GROUP BY l.locationid
        ORDER BY average_score DESC, average_total DESC,
        show_count DESC, l.venue ASC;
    """

    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    _average_scores = []
    for row in result:
        _average_scores.append(
            {
                "id": row["locationid"],
                "slug": row["locationslug"],
                "venue": row["venue"],
                "city": row["city"],
                "state": row["state"],
                "average_score": round(Decimal(row["average_score"]), 5),
                "average_total": round(Decimal(row["average_total"]), 5),
                "show_count": int(row["show_count"]),
            }
        )

    return _average_scores
