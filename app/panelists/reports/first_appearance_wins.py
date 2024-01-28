# Copyright (c) 2018-2024 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Panelist First Appearance Wins."""
from decimal import Decimal

from flask import current_app
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection


def retrieve_panelists_first_appearance_wins(
    database_connection: MySQLConnection | PooledMySQLConnection,
    use_decimal_scores: bool = False,
) -> dict[str, str | int | Decimal]:
    """Returns a dictionary containing wins or tied for first for panelists' first appearance."""
    if (
        use_decimal_scores
        and not current_app.config["app_settings"]["has_decimal_scores_column"]
    ):
        return None

    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT DISTINCT p.panelistslug
        FROM ww_showpnlmap pm
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        JOIN ww_shows s ON s.showid = pm.showid
        WHERE s.bestof = 0
        AND s.repeatshowid IS NULL
        AND pm.showpnlrank IN ('1', '1t')
        ORDER BY p.panelistslug;
        """
    cursor = database_connection.cursor(named_tuple=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    panelist_slugs = [panelist.panelistslug for panelist in result]

    panelists = {}
    for panelist_slug in panelist_slugs:
        cursor = database_connection.cursor(named_tuple=True)
        if use_decimal_scores:
            query = """
                SELECT p.panelist, s.showid, s.showdate, pm.panelistlrndstart,
                pm.panelistlrndcorrect, pm.panelistscore, pm.panelistscore_decimal,
                pm.showpnlrank
                FROM ww_showpnlmap pm
                JOIN ww_panelists p ON p.panelistid = pm.panelistid
                JOIN ww_shows s ON s.showid = pm.showid
                WHERE p.panelistslug = %s
                AND s.bestof = 0 AND s.repeatshowid IS NULL
                ORDER BY s.showdate ASC
                LIMIT 1;
                """
        else:
            query = """
                SELECT p.panelist, s.showid, s.showdate, pm.panelistlrndstart,
                pm.panelistlrndcorrect, pm.panelistscore, pm.showpnlrank
                FROM ww_showpnlmap pm
                JOIN ww_panelists p ON p.panelistid = pm.panelistid
                JOIN ww_shows s ON s.showid = pm.showid
                WHERE p.panelistslug = %s
                AND s.bestof = 0 AND s.repeatshowid IS NULL
                ORDER BY s.showdate ASC
                LIMIT 1;
                """
        cursor.execute(query, (panelist_slug,))
        result = cursor.fetchone()
        cursor.close()

        if not result:
            return None

        if result.showpnlrank == "1" or result.showpnlrank == "1t":
            if use_decimal_scores:
                panelists[panelist_slug] = {
                    "name": result.panelist,
                    "show_date": result.showdate.isoformat(),
                    "start": result.panelistlrndstart,
                    "correct": result.panelistlrndcorrect,
                    "score": result.panelistscore,
                    "score_decimal": result.panelistscore_decimal,
                    "rank": result.showpnlrank,
                }
            else:
                panelists[panelist_slug] = {
                    "name": result.panelist,
                    "show_date": result.showdate.isoformat(),
                    "start": result.panelistlrndstart,
                    "correct": result.panelistlrndcorrect,
                    "score": result.panelistscore,
                    "rank": result.showpnlrank,
                }

    return panelists
