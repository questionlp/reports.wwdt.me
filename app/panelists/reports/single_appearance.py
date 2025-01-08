# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Panelist Single Appearance Report Functions."""
from typing import Any

from flask import current_app
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection


def retrieve_single_appearances(
    database_connection: MySQLConnection | PooledMySQLConnection,
    use_decimal_scores: bool = False,
) -> list[dict[str, Any]]:
    """Retrieve a list of panelists that have only made a single appearance on the show."""
    if (
        use_decimal_scores
        and not current_app.config["app_settings"]["has_decimal_scores_column"]
    ):
        return None

    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT p.panelistid
        FROM ww_showpnlmap pm
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        JOIN ww_shows s ON s.showid = pm.showid
        WHERE s.bestof = 0 AND s.repeatshowid IS NULL
        GROUP BY p.panelistid
        HAVING COUNT(p.panelistid) = 1
        ORDER BY p.panelistid;
        """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()

    if not results:
        return None

    list_panelists = []
    for row in results:
        list_panelists.append(row["panelistid"])

    if use_decimal_scores:
        query = f"""
            SELECT p.panelist, p.panelistslug, s.showdate,
            pm.panelistscore_decimal AS score, pm.showpnlrank
            FROM ww_showpnlmap pm
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE pm.panelistid IN ({", ".join(str(ids) for ids in list_panelists)})
            AND s.bestof = 0 AND s.repeatshowid IS NULL
            ORDER BY p.panelist ASC;
            """
    else:
        query = f"""
            SELECT p.panelist, p.panelistslug, s.showdate,
            pm.panelistscore AS score, pm.showpnlrank FROM ww_showpnlmap pm
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE pm.panelistid IN ({", ".join(str(ids) for ids in list_panelists)})
            AND s.bestof = 0 AND s.repeatshowid IS NULL
            ORDER BY p.panelist ASC;
            """

    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    panelists = []
    for row in result:
        panelists.append(
            {
                "name": row["panelist"],
                "slug": row["panelistslug"],
                "appearance": row["showdate"].isoformat(),
                "score": row["score"],
                "rank": row["showpnlrank"],
            }
        )

    return panelists
