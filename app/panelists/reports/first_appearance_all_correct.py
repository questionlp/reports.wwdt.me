# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Panelist First Appearance All Correct."""

from decimal import Decimal

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection


def retrieve_panelists_first_appearance_all_correct(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> dict[str, str | int | Decimal]:
    """Returns panelists answering all Lightning questions correct in first appearance."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT panelistid, panelist, panelistslug
        FROM ww_panelists
        WHERE panelistslug <> 'multiple'
        ORDER BY panelist;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    panelist_slugs = [panelist["panelistslug"] for panelist in result]

    panelists = {}
    for panelist_slug in panelist_slugs:
        cursor = database_connection.cursor(dictionary=True)
        query = """
            SELECT p.panelist, s.showid, s.showdate,
            pm.panelistlrndstart_decimal, pm.panelistlrndcorrect_decimal,
            pm.panelistscore_decimal, pm.showpnlrank
            FROM ww_showpnlmap pm
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE p.panelistslug = %s
            AND pm.panelistlrndcorrect_decimal IS NOT NULL
            AND s.bestof = 0 AND s.repeatshowid IS NULL
            ORDER BY s.showdate ASC
            LIMIT 1;
        """
        cursor.execute(query, (panelist_slug,))
        result = cursor.fetchone()
        cursor.close()

        if result and result["panelistlrndcorrect_decimal"] >= 8:
            panelists[panelist_slug] = {
                "name": result["panelist"],
                "show_date": result["showdate"].isoformat(),
                "start": result["panelistlrndstart_decimal"],
                "correct": result["panelistlrndcorrect_decimal"],
                "score": result["panelistscore_decimal"],
                "rank": result["showpnlrank"],
            }

    return panelists
