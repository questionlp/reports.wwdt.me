# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Panelist First Appearances."""

from decimal import Decimal

from flask import current_app
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection


def retrieve_panelists_first_appearance(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> dict[str, dict[str | int | Decimal]]:
    """Returns a dictionary of panelists' first appearances.

    The dictionary uses panelist slug string as keys with panelist's first
    appearance information as a dictionary as the key value.
    """
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

    panelists = {}
    for row in result:
        _id = row["panelistid"]
        _slug = row["panelistslug"]

        query = """
            SELECT s.showdate, s.bestof, s.repeatshowid,
            pm.panelistlrndstart, pm.panelistlrndstart_decimal,
            pm.panelistlrndcorrect, pm.panelistlrndcorrect_decimal,
            pm.panelistscore, pm.panelistscore_decimal, pm.showpnlrank
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE pm.panelistid = %s
            ORDER BY s.showdate ASC
            LIMIT 1;
        """

        cursor = database_connection.cursor(dictionary=True)
        cursor.execute(query, (_id,))
        result_app = cursor.fetchone()
        cursor.close()

        if result_app:
            panelists[_slug] = {
                "name": row["panelist"],
                "slug": _slug,
                "show_date": result_app["showdate"].isoformat(),
                "start": result_app["panelistlrndstart"],
                "start_decimal": result_app["panelistlrndstart_decimal"],
                "correct": result_app["panelistlrndcorrect"],
                "correct_decimal": result_app["panelistlrndcorrect_decimal"],
                "score": result_app["panelistscore"],
                "score_decimal": result_app["panelistscore_decimal"],
                "rank": result_app["showpnlrank"],
            }

    return panelists
