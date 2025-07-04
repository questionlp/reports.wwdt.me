# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Panelist Perfect Scores Report Functions."""

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from .common import retrieve_panelists_id_key


def retrieve_perfect_score_counts(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> dict[str, str | int]:
    """Returns a dictionary with counts of how many times panelists have scored a "perfect" score.

    A "perfect" score is one that greater than or equals to 20 points. Excludes
    Best Of and repeat shows.
    """
    if not database_connection.is_connected():
        database_connection.reconnect()

    _panelists = retrieve_panelists_id_key(database_connection=database_connection)

    # Get panelists who have scored 20 points
    query = """
        SELECT p.panelistid, COUNT(p.panelistid) AS score_count
        FROM ww_showpnlmap pm
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        JOIN ww_shows s ON s.showid = pm.showid
        WHERE pm.panelistscore_decimal = 20
        AND s.bestof = 0 AND s.repeatshowid IS NULL
        GROUP BY p.panelistid
        ORDER BY COUNT(p.panelistid) DESC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    results_eq_20 = cursor.fetchall()
    cursor.close()

    # Get panelists who have scored 20 or more points
    query = """
        SELECT p.panelistid, COUNT(p.panelistid) AS score_count
        FROM ww_showpnlmap pm
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        JOIN ww_shows s ON s.showid = pm.showid
        WHERE pm.panelistscore_decimal >= 20
        AND s.bestof = 0 AND s.repeatshowid IS NULL
        GROUP BY p.panelistid
        ORDER BY COUNT(p.panelistid) DESC, p.panelist ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    results_ge_20 = cursor.fetchall()
    cursor.close()

    if not results_eq_20 and not results_ge_20:
        return None

    panelists = {}
    for row in results_ge_20:
        panelists[row["panelistid"]] = {
            "name": _panelists[row["panelistid"]]["name"],
            "slug": _panelists[row["panelistid"]]["slug"],
            "more_perfect": row["score_count"],
            "perfect": None,
        }

    for row in results_eq_20:
        panelists[row["panelistid"]]["perfect"] = row["score_count"]

    return panelists
