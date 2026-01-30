# Copyright (c) 2018-2026 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Panelist First Wins."""

from decimal import Decimal

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from .common import retrieve_panelists


def retrieve_panelists_first_wins(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> dict[str, str | int | Decimal]:
    """Returns a dictionary of each panelist's first outright or overall win.

    Overall win includes winning outright or being tied for first.
    """
    if not database_connection.is_connected():
        database_connection.reconnect()

    _all_panelists = retrieve_panelists(database_connection=database_connection)
    panelists = {}
    for panelist in _all_panelists:
        _panelist_slug = panelist["slug"]
        panelists[_panelist_slug] = {
            "name": panelist["name"],
            "slug": _panelist_slug,
        }

        query = """
            SELECT p.panelist, p.panelistslug, s.showdate,
            pm.panelistscore_decimal, pm.showpnlrank
            FROM ww_showpnlmap pm
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE p.panelistslug = %s AND pm.showpnlrank = '1'
            AND s.bestof = 0 and s.repeatshowid IS NULL
            ORDER BY s.showdate
            LIMIT 1
        """
        cursor = database_connection.cursor(dictionary=True)
        cursor.execute(query, (_panelist_slug,))
        first_outright_wins_result = cursor.fetchone()
        cursor.close()

        if not first_outright_wins_result:
            panelists[_panelist_slug]["first_win"] = None
        else:
            panelists[_panelist_slug]["first_win"] = {
                "show_date": first_outright_wins_result["showdate"].isoformat(),
                "score": first_outright_wins_result["panelistscore_decimal"],
                "rank": first_outright_wins_result["showpnlrank"],
            }

        query = """
            SELECT p.panelist, p.panelistslug, s.showdate,
            pm.panelistscore_decimal, pm.showpnlrank
            FROM ww_showpnlmap pm
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE p.panelistslug = %s AND pm.showpnlrank IN ('1', '1t')
            AND s.bestof = 0 and s.repeatshowid IS NULL
            ORDER BY s.showdate
            LIMIT 1
        """
        cursor = database_connection.cursor(dictionary=True)
        cursor.execute(query, (_panelist_slug,))
        first_overall_wins_result = cursor.fetchone()
        cursor.close()

        if not first_overall_wins_result:
            panelists[_panelist_slug]["first_overall_win"] = None
        else:
            panelists[_panelist_slug]["first_overall_win"] = {
                "show_date": first_overall_wins_result["showdate"].isoformat(),
                "score": first_overall_wins_result["panelistscore_decimal"],
                "rank": first_overall_wins_result["showpnlrank"],
            }

    return panelists
