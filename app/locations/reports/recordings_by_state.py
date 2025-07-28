# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Location Recording Counts by State/Province Report Functions."""

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection


def retrieve_recording_counts_by_state(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> dict[str, dict[str, int]]:
    """Retrieve a count of recordings broken down by state/province."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT state, name, COUNT(name) AS count
        FROM ww_showlocationmap lm
        JOIN ww_locations l ON l.locationid = lm.locationid
        JOIN ww_postal_abbreviations pa ON pa.postal_abbreviation = l.state
        JOIN ww_shows s ON s.showid = lm.showid
        GROUP BY state, name
        ORDER BY COUNT(name) DESC
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    all_results = cursor.fetchall()
    cursor.close()

    query = """
        SELECT state, name, COUNT(name) AS count
        FROM ww_showlocationmap lm
        JOIN ww_locations l ON l.locationid = lm.locationid
        JOIN ww_postal_abbreviations pa ON pa.postal_abbreviation = l.state
        JOIN ww_shows s ON s.showid = lm.showid
        WHERE s.bestof = 0 AND s.repeatshowid IS NULL
        GROUP BY state, name
        ORDER BY COUNT(name) DESC
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    regular_results = cursor.fetchall()
    cursor.close()

    query = """
        SELECT state, name, COUNT(name) AS count
        FROM ww_showlocationmap lm
        JOIN ww_locations l ON l.locationid = lm.locationid
        JOIN ww_postal_abbreviations pa ON pa.postal_abbreviation = l.state
        JOIN ww_shows s ON s.showid = lm.showid
        WHERE s.bestof = 1 AND s.repeatshowid IS NULL
        GROUP BY state, name
        ORDER BY COUNT(name) DESC
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    best_ofs_results = cursor.fetchall()
    cursor.close()

    query = """
        SELECT state, name, COUNT(name) AS count
        FROM ww_showlocationmap lm
        JOIN ww_locations l ON l.locationid = lm.locationid
        JOIN ww_postal_abbreviations pa ON pa.postal_abbreviation = l.state
        JOIN ww_shows s ON s.showid = lm.showid
        WHERE s.bestof = 1 AND s.repeatshowid IS NOT NULL
        GROUP BY state, name
        ORDER BY COUNT(name) DESC
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    repeat_best_ofs_results = cursor.fetchall()
    cursor.close()

    query = """
        SELECT state, name, COUNT(name) AS count
        FROM ww_showlocationmap lm
        JOIN ww_locations l ON l.locationid = lm.locationid
        JOIN ww_postal_abbreviations pa ON pa.postal_abbreviation = l.state
        JOIN ww_shows s ON s.showid = lm.showid
        WHERE s.bestof = 0 AND s.repeatshowid IS NOT NULL
        GROUP BY state, name
        ORDER BY COUNT(name) DESC
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    repeats_results = cursor.fetchall()
    cursor.close()

    _states = {}
    for row in all_results:
        _states[row["state"]] = {
            "state": row["state"],
            "name": row["name"],
            "regular": 0,
            "best_ofs": 0,
            "repeat_best_ofs": 0,
            "repeats": 0,
            "all": row["count"],
        }

    for row in regular_results:
        _states[row["state"]]["regular"] = row["count"]

    for row in best_ofs_results:
        _states[row["state"]]["best_ofs"] = row["count"]

    for row in repeat_best_ofs_results:
        _states[row["state"]]["repeat_best_ofs"] = row["count"]

    for row in repeats_results:
        _states[row["state"]]["repeats"] = row["count"]

    return _states
