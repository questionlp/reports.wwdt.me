# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Location Recordings by Year Report Functions."""

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from app.panelists.reports.appearances_by_year import retrieve_all_years


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
        WHERE YEAR(s.showdate) = %s
        GROUP BY l.locationid, l.locationslug
        ORDER BY COUNT(l.locationid) DESC, l.locationslug ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (year,))
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
        WHERE YEAR(s.showdate) = %s AND s.bestof = 0
        AND s.repeatshowid IS NULL
        GROUP BY l.locationid, l.locationslug
        ORDER BY COUNT(l.locationid) DESC, l.locationslug ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (year,))
    regular_results = cursor.fetchall()
    cursor.close()

    query = """
        SELECT l.locationid, l.city, l.state, l.venue, l.locationslug,
        COUNT(l.locationid) AS count
        FROM ww_showlocationmap lm
        JOIN ww_shows s ON s.showid = lm.showid
        JOIN ww_locations l ON l.locationid = lm.locationid
        WHERE YEAR(s.showdate) = %s AND s.bestof = 1
        AND s.repeatshowid IS NULL
        GROUP BY l.locationid, l.locationslug
        ORDER BY COUNT(l.locationid) DESC, l.locationslug ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (year,))
    best_ofs_results = cursor.fetchall()
    cursor.close()

    query = """
        SELECT l.locationid, l.city, l.state, l.venue, l.locationslug,
        COUNT(l.locationid) AS count
        FROM ww_showlocationmap lm
        JOIN ww_shows s ON s.showid = lm.showid
        JOIN ww_locations l ON l.locationid = lm.locationid
        WHERE YEAR(s.showdate) = %s AND s.bestof = 1
        AND s.repeatshowid IS NOT NULL
        GROUP BY l.locationid, l.locationslug
        ORDER BY COUNT(l.locationid) DESC, l.locationslug ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (year,))
    repeat_best_ofs_results = cursor.fetchall()
    cursor.close()

    query = """
        SELECT l.locationid, l.city, l.state, l.venue, l.locationslug,
        COUNT(l.locationid) AS count
        FROM ww_showlocationmap lm
        JOIN ww_shows s ON s.showid = lm.showid
        JOIN ww_locations l ON l.locationid = lm.locationid
        WHERE YEAR(s.showdate) = %s AND s.bestof = 1
        AND s.repeatshowid IS NULL
        GROUP BY l.locationid, l.locationslug
        ORDER BY COUNT(l.locationid) DESC, l.locationslug ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (year,))
    repeats_results = cursor.fetchall()
    cursor.close()

    _appearances = {}
    for row in all_results:
        _appearances[row["locationslug"]] = {
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
        _appearances[row["locationslug"]]["regular"] = row["count"]

    for row in best_ofs_results:
        _appearances[row["locationslug"]]["best_ofs"] = row["count"]

    for row in repeat_best_ofs_results:
        _appearances[row["locationslug"]]["repeat_best_ofs"] = row["count"]

    for row in repeats_results:
        _appearances[row["locationslug"]]["repeats"] = row["count"]

    return _appearances


def retrieve_all_recording_counts_by_year(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> dict[int, dict[str, str | int | None]]:
    """Retrieve all recording counts for all locations from the database."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    _years_list = retrieve_all_years(database_connection=database_connection)

    if not _years_list:
        return None

    _years = {}
    for _year in _years_list:
        _recordings = retrieve_recording_counts_by_year(
            year=_year, database_connection=database_connection
        )

        if _recordings:
            _years[_year] = _recordings
        else:
            _years[_year] = None

    return _years
