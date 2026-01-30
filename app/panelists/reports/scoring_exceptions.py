# Copyright (c) 2018-2026 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Panelist Scoring Exceptions and Anomalies."""

from decimal import Decimal

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection


def retrieve_panelist_scoring_exceptions(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict[str, str | Decimal]]:
    """Returns a list of dictionaries with panelist scoring exceptions.

    Each dictionary contains the show date, panelist name, panelist
    slug string, Lightning Fill In The Blank scoring information and
    notes for that show.
    """
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = (
        "SELECT s.showdate, p.panelist, p.panelistslug, "
        "pm.panelistlrndstart_decimal, pm.panelistlrndcorrect_decimal, "
        "pm.panelistscore_decimal, pm.showpnlrank, sn.shownotes "
        "FROM ww_showpnlmap pm "
        "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
        "JOIN ww_shows s ON s.showid = pm.showid "
        "JOIN ww_shownotes sn ON sn.showid = pm.showid "
        "WHERE s.bestof = 0 AND s.repeatshowid IS NULL "
        "AND pm.panelistlrndstart_decimal IS NOT NULL "
        "AND pm.panelistlrndcorrect_decimal IS NOT NULL "
        "AND pm.panelistscore_decimal IS NOT NULL "
        "AND ((pm.panelistlrndcorrect_decimal * 2) + pm.panelistlrndstart_decimal) "
        "<> pm.panelistscore_decimal "
        "ORDER BY s.showdate;"
    )
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    scoring_exceptions = []
    for row in result:
        scoring_exception = {
            "show_date": row["showdate"].isoformat(),
            "name": row["panelist"],
            "slug": row["panelistslug"],
            "start": row["panelistlrndstart_decimal"],
            "correct": row["panelistlrndcorrect_decimal"],
            "score": row["panelistscore_decimal"],
            "rank": row["showpnlrank"],
            "show_notes": row["shownotes"],
        }
        scoring_exceptions.append(scoring_exception)

    return scoring_exceptions
