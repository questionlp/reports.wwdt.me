# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Location Recordings by Year Report Functions."""

from typing import Any

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


def retrieve_location_recording_counts(
    location_id: int, database_connection: MySQLConnection | PooledMySQLConnection
) -> list[dict[str | int, int]]:
    """Retrieve yearly recording counts for a given location ID.

    Appearance counts exclude both Best Of and repeat shows.
    """
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT YEAR(s.showdate) AS year, COUNT(l.locationid) AS count
        FROM ww_showlocationmap lm
        JOIN ww_shows s ON s.showid = lm.showid
        JOIN ww_locations l ON l.locationid = lm.locationid
        WHERE lm.locationid = %s AND s.bestof = 0
        AND s.repeatshowid IS NULL
        GROUP BY l.locationid, YEAR(s.showdate)
        ORDER BY l.locationslug ASC, YEAR(s.showdate) ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (location_id,))
    results = cursor.fetchall()
    cursor.close()

    if not results:
        return None

    _appearances = {}
    total_appearances = 0
    for row in results:
        _appearances[row["year"]] = row["count"]
        total_appearances += row["count"]

    _appearances["total"] = total_appearances
    return _appearances


def retrieve_location_recording_counts_all(
    location_id: int, database_connection: MySQLConnection | PooledMySQLConnection
) -> list[dict[str | int, int]]:
    """Retrieve yearly recording counts for a given location ID.

    Appearance counts include both Best Of and repeat shows.
    """
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT YEAR(s.showdate) AS year, COUNT(l.locationid) AS count
        FROM ww_showlocationmap lm
        JOIN ww_shows s ON s.showid = lm.showid
        JOIN ww_locations l ON l.locationid = lm.locationid
        WHERE lm.locationid = %s
        GROUP BY l.locationid, YEAR(s.showdate)
        ORDER BY l.locationslug ASC, YEAR(s.showdate) ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (location_id,))
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    _appearances = {}
    total_appearances = 0
    for row in result:
        _appearances[row["year"]] = row["count"]
        total_appearances += row["count"]

    _appearances["total"] = total_appearances
    return _appearances


def retrieve_all_recording_counts(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict[str, Any]]:
    """Retrieve all recoding counts for all locations from the database."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT DISTINCT l.locationid, l.venue, l.city, l.state,
        l.locationslug
        FROM ww_locationsmap lm
        JOIN ww_locations l ON l.locationid = lm.locationid
        JOIN ww_shows s ON s.showid = lm.showid
        WHERE s.bestof = 0 AND s.repeatshowid IS NULL
        ORDER BY l.venue ASC, l.city ASC, l.state ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    _hosts = []
    for row in result:
        location_id = row["locationid"]
        _hosts.append(
            {
                "name": row["venue"],
                "city": row["city"],
                "state": row["state"],
                "slug": row["locationslug"],
                "regular_recordings": retrieve_location_recording_counts(
                    location_id=location_id, database_connection=database_connection
                ),
                "all_recordings": retrieve_location_recording_counts_all(
                    location_id=location_id, database_connection=database_connection
                ),
            }
        )

    return _hosts


def retrieve_all_recordings_by_year(
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
