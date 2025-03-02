# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Location Recordings by Year Report Functions."""

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection


def retrieve_recording_counts_by_year(
    year: int, database_connection: MySQLConnection | PooledMySQLConnection
) -> dict[str, dict[str, str | int | None]]:
    """Retrieve location recording counts for a given year."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT l.locationid, l.city, l.state, l.venue, l.locationslug,
        COUNT(l.locationid) AS count
        FROM ww_showlocationmap lm
        JOIN ww_shows s ON s.showid = lm.showid
        JOIN ww_locations l ON l.locationid = lm.locationid
        WHERE YEAR(s.showdate) = %s AND s.bestof = 0
        AND s.repeatshowid IS NULL
        GROUP BY l.locationid, l.locationslug
        ORDER BY COUNT(l.locationid) DESC, l.locationslug ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (year,))
    results = cursor.fetchall()
    cursor.close()

    all_query = """
        SELECT l.locationid, l.city, l.state, l.venue, l.locationslug,
        COUNT(l.locationid) AS count
        FROM ww_showlocationmap lm
        JOIN ww_shows s ON s.showid = lm.showid
        JOIN ww_locations l ON l.locationid = lm.locationid
        WHERE YEAR(s.showdate) = %s
        GROUP BY l.locationid, l.locationslug
        ORDER BY COUNT(l.locationid) DESC, l.locationslug ASC;
    """
    all_cursor = database_connection.cursor(dictionary=True)
    all_cursor.execute(all_query, (year,))
    all_results = all_cursor.fetchall()
    all_cursor.close()

    if not results or not all_results:
        return None

    _appearances = {}
    for row in results:
        _appearances[row["locationslug"]] = {
            "venue": row["venue"],
            "city": row["city"],
            "state": row["state"],
            "slug": row["locationslug"],
            "regular_recordings": row["count"],
        }

    for row in all_results:
        if row["locationslug"] not in _appearances:
            _appearances[row["locationslug"]] = {
                "venue": row["venue"],
                "city": row["city"],
                "state": row["state"],
                "slug": row["locationslug"],
                "regular_recordings": 0,
                "all_recordings": row["count"],
            }
        else:
            _appearances[row["locationslug"]]["all_recordings"] = row["count"]

    return _appearances
