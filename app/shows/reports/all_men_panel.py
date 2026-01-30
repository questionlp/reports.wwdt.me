# Copyright (c) 2018-2026 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM All Men Panel Report Functions."""

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from .all_women_panel import retrieve_show_details


def retrieve_shows_all_men_panel(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict]:
    """Retrieves details from all shows that have had an all men panel."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT pm.showid
        FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        WHERE s.bestof = 0 AND s.repeatshowid IS NULL
        AND s.showdate <> '2018-10-27'
        AND p.panelistgender = 'M'
        GROUP BY pm.showid
        HAVING COUNT(s.showid) = 3
        ORDER BY s.showdate ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    shows = []
    for row in result:
        show_id = row["showid"]
        show_details = retrieve_show_details(
            show_id=show_id,
            database_connection=database_connection,
        )
        if show_details:
            shows.append(show_details)

    return shows
