# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Panelist Appearances Report Functions."""

from typing import Any

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from . import common


def retrieve_first_most_recent_appearances(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict[str, Any]]:
    """Retrieve first/most recent appearances for both regular and all shows for all panelists."""
    panelists = common.retrieve_panelists(database_connection=database_connection)

    if not panelists:
        return None

    panelist_appearances = {}
    for panelist in panelists:
        panelist_appearances[panelist["slug"]] = {
            "name": panelist["name"],
            "slug": panelist["slug"],
            "first": None,
            "most_recent": None,
            "count": 0,
            "first_all": None,
            "most_recent_all": None,
            "count_all": 0,
        }

    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT p.panelist, p.panelistslug,
        MIN(s.showdate) AS min, MAX(s.showdate) AS max
        FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        WHERE s.bestof = 0
        AND s.repeatshowid IS null
        AND p.panelist <> '<Multiple>'
        GROUP BY p.panelistid
        ORDER BY p.panelist ASC;
        """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    for row in result:
        panelist_appearances[row["panelistslug"]]["first"] = row["min"].isoformat()
        panelist_appearances[row["panelistslug"]]["most_recent"] = row[
            "max"
        ].isoformat()

    query = """
        SELECT p.panelist, p.panelistslug, COUNT(pm.panelistid) AS count
        FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        WHERE s.bestof = 0 AND s.repeatshowid IS NULL
        AND p.panelist <> '<Multiple>'
        GROUP BY p.panelistid
        ORDER BY p.panelist ASC;
        """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    for row in result:
        panelist_appearances[row["panelistslug"]]["count"] = row["count"]

    query = """
        SELECT p.panelist, p.panelistslug, COUNT(pm.panelistid) AS count
        FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        WHERE p.panelist <> '<Multiple>'
        GROUP BY p.panelistid
        ORDER BY p.panelist ASC;
        """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    for row in result:
        panelist_appearances[row["panelistslug"]]["count_all"] = row["count"]

    query = """
        SELECT p.panelist, p.panelistslug,
        MIN(s.showdate) AS min, MAX(s.showdate) AS max
        FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        WHERE p.panelist <> '<Multiple>'
        GROUP BY p.panelistid
        ORDER BY p.panelist ASC;
        """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return panelist_appearances

    for row in result:
        panelist_appearances[row["panelistslug"]]["first_all"] = row["min"].isoformat()
        panelist_appearances[row["panelistslug"]]["most_recent_all"] = row[
            "max"
        ].isoformat()

    return panelist_appearances
