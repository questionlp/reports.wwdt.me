# Copyright (c) 2018-2026 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Location Home vs Away Report Functions."""

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection


def retrieve_location_home_vs_away(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict[str, int]] | None:
    """Retrieve counts of home versus away shows broken down by year."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT DISTINCT YEAR(showdate) FROM ww_shows
        ORDER BY YEAR(showdate) ASC;
    """
    cursor = database_connection.cursor(dictionary=False)
    cursor.execute(query)
    results = cursor.fetchall()

    if not results:
        return None

    years = [year[0] for year in results]

    counts = []
    for year in years:
        query = """
            SELECT (
                SELECT COUNT(s.showid)
                FROM ww_shows s
                JOIN ww_showlocationmap lm ON lm.showid = s.showid
                JOIN ww_locations l ON l.locationid = lm.locationid
                WHERE YEAR(s.showdate) = %s
                AND s.bestof = 0
                AND s.repeatshowid IS NULL
                AND l.city = 'Chicago'
                AND l.state = 'IL'
            )  AS 'home', (
                SELECT COUNT(s.showid)
                FROM ww_shows s
                JOIN ww_showlocationmap lm ON lm.showid = s.showid
                JOIN ww_locations l ON l.locationid = lm.locationid
                WHERE YEAR(s.showdate) = %s
                AND s.bestof = 0
                AND s.repeatshowid IS NULL
                AND l.city <> 'Chicago'
                AND l.state <> 'IL'
            ) AS 'away', (
                SELECT COUNT(s.showid)
                FROM ww_shows s
                JOIN ww_showlocationmap lm ON lm.showid = s.showid
                JOIN ww_locations l ON l.locationid = lm.locationid
                WHERE YEAR(s.showdate) = %s
                AND s.bestof = 0
                AND s.repeatshowid IS NULL
                AND lm.locationid = 148
            ) AS 'studios';
        """
        cursor = database_connection.cursor(dictionary=True)
        cursor.execute(
            query,
            (
                year,
                year,
                year,
            ),
        )
        result = cursor.fetchone()

        if not result:
            counts.append({"year": year, "home": None, "away": None})
        else:
            counts.append(
                {
                    "year": year,
                    "home": result["home"],
                    "away": result["away"],
                    "studios": result["studios"],
                }
            )

    return counts
