# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Show with Panelists Having Matching Initials Report Functions."""

from flask import current_app
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from .all_women_panel import retrieve_show_details


def retrieve_shows_panelists_matching_initials(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict]:
    """Retrieves details from shows where each panelists has matching initials."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    panelists_double_initials = current_app.config["app_settings"].get(
        "panelists_double_initials", None
    )
    if not panelists_double_initials or not isinstance(panelists_double_initials, list):
        return None

    query = f"""
        SELECT s.showid, COUNT(s.showid)
        FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        WHERE s.bestof = 0 AND s.repeatshowid IS NULL
        AND s.showdate <> '2018-10-27'
        AND p.panelistslug IN ({", ".join("'" + slug + "'" for slug in panelists_double_initials)})
        GROUP BY s.showid
        HAVING COUNT(s.showid) >= 3
        ORDER BY s.showdate ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()

    if not results:
        return None

    shows = []
    for row in results:
        show_id = row["showid"]
        show_details = retrieve_show_details(
            show_id=show_id, database_connection=database_connection
        )
        if show_details:
            shows.append(show_details)

    return shows
