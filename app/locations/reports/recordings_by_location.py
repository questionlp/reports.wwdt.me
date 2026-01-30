# Copyright (c) 2018-2026 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Location Recordings by Location Report Functions."""

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from app.panelists.reports.appearances_by_year import retrieve_all_years


def retrieve_recording_counts_by_location(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> dict[str, dict[str, str | int | None]]:
    """Retrieve recording counts for all available locations."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT l.locationid, l.city, l.state, l.venue, l.locationslug,
        COUNT(l.locationid) AS count
        FROM ww_showlocationmap lm
        JOIN ww_shows s ON s.showid = lm.showid
        JOIN ww_locations l ON l.locationid = lm.locationid
        WHERE l.locationid <> 3
        GROUP BY l.locationid, l.locationslug
        ORDER BY COUNT(l.locationid) DESC, l.locationslug ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    all_results = cursor.fetchall()
    cursor.close()

    if not all_results:
        return None

    query = """
        SELECT l.locationid, l.city, l.state, l.venue, l.locationslug,
        COUNT(l.locationid) AS count
        FROM ww_showlocationmap lm
        JOIN ww_shows s ON s.showid = lm.showid
        JOIN ww_locations l ON l.locationid = lm.locationid
        WHERE l.locationid <> 3 AND s.bestof = 0 AND s.repeatshowid IS NULL
        GROUP BY l.locationid, l.locationslug
        ORDER BY COUNT(l.locationid) DESC, l.locationslug ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    regular_results = cursor.fetchall()
    cursor.close()

    query = """
        SELECT l.locationid, l.city, l.state, l.venue, l.locationslug,
        COUNT(l.locationid) AS count
        FROM ww_showlocationmap lm
        JOIN ww_shows s ON s.showid = lm.showid
        JOIN ww_locations l ON l.locationid = lm.locationid
        WHERE l.locationid <> 3 AND s.bestof = 1 AND s.repeatshowid IS NULL
        GROUP BY l.locationid, l.locationslug
        ORDER BY COUNT(l.locationid) DESC, l.locationslug ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    best_ofs_results = cursor.fetchall()
    cursor.close()

    query = """
        SELECT l.locationid, l.city, l.state, l.venue, l.locationslug,
        COUNT(l.locationid) AS count
        FROM ww_showlocationmap lm
        JOIN ww_shows s ON s.showid = lm.showid
        JOIN ww_locations l ON l.locationid = lm.locationid
        WHERE l.locationid <> 3 AND s.bestof = 1 AND s.repeatshowid IS NOT NULL
        GROUP BY l.locationid, l.locationslug
        ORDER BY COUNT(l.locationid) DESC, l.locationslug ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    repeat_best_ofs_results = cursor.fetchall()
    cursor.close()

    query = """
        SELECT l.locationid, l.city, l.state, l.venue, l.locationslug,
        COUNT(l.locationid) AS count
        FROM ww_showlocationmap lm
        JOIN ww_shows s ON s.showid = lm.showid
        JOIN ww_locations l ON l.locationid = lm.locationid
        WHERE l.locationid <> 3 AND s.bestof = 0 AND s.repeatshowid IS NOT NULL
        GROUP BY l.locationid, l.locationslug
        ORDER BY COUNT(l.locationid) DESC, l.locationslug ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    repeats_results = cursor.fetchall()
    cursor.close()

    _recordings = {}
    for row in all_results:
        _recordings[row["locationslug"]] = {
            "venue": row["venue"],
            "city": row["city"],
            "state": row["state"],
            "slug": row["locationslug"],
            "regular": 0,
            "best_ofs": 0,
            "repeat_best_ofs": 0,
            "repeats": 0,
            "all": row["count"],
        }

    for row in regular_results:
        _recordings[row["locationslug"]]["regular"] = row["count"]

    for row in best_ofs_results:
        _recordings[row["locationslug"]]["best_ofs"] = row["count"]

    for row in repeat_best_ofs_results:
        _recordings[row["locationslug"]]["repeat_best_ofs"] = row["count"]

    for row in repeats_results:
        _recordings[row["locationslug"]]["repeats"] = row["count"]

    return _recordings
