# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM All Women Panel Report Functions."""

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection


def retrieve_show_details(
    show_id: int,
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> dict:
    """Retrieves host, scorekeeper, panelist, guest and location information."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    # Retrieve host, scorekeeper and guest
    query = """
        SELECT s.showdate, h.host, sk.scorekeeper, g.guest,
        gm.guestscore, gm.exception
        FROM ww_showhostmap hm
        JOIN ww_shows s ON s.showid = hm.showid
        JOIN ww_hosts h ON h.hostid = hm.hostid
        JOIN ww_showskmap skm ON skm.showid = hm.showid
        JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid
        JOIN ww_showguestmap gm ON gm.showid = hm.showid
        JOIN ww_guests g ON g.guestid = gm.guestid
        WHERE hm.showid = %s;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (show_id,))
    result = cursor.fetchone()

    if not result:
        return None

    show_details = {
        "date": result["showdate"].isoformat(),
        "host": result["host"],
        "scorekeeper": result["scorekeeper"],
        "guest": {
            "name": result["guest"],
            "score": result["guestscore"],
            "exception": bool(result["exception"]),
        },
    }

    # Retrieve show location details
    query = """
        SELECT l.city, l.state, l.venue
        FROM ww_showlocationmap lm
        JOIN ww_locations l ON l.locationid = lm.locationid
        WHERE lm.showid = %s;
        """
    cursor.execute(query, (show_id,))
    result = cursor.fetchone()

    if not result:
        show_details["location"] = None
    else:
        show_details["location"] = {
            "city": result["city"],
            "state": result["state"],
            "venue": result["venue"],
        }

    # Retrieve panelists and their respective show rank and score
    query = """
        SELECT p.panelist, pm.panelistscore_decimal
        FROM ww_showpnlmap pm
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        WHERE pm.showid = %s
        ORDER BY pm.panelistscore DESC, pm.showpnlrank ASC;
    """
    cursor.execute(query, (show_id,))
    result = cursor.fetchall()
    cursor.close()

    if not result:
        show_details["panelists"] = None
    else:
        panelists = []
        for row in result:
            panelists.append(
                {
                    "name": row["panelist"],
                    "score": row["panelistscore_decimal"],
                }
            )

        show_details["panelists"] = panelists

    return show_details


def retrieve_shows_all_women_panel(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict]:
    """Retrieves details from all shows that have had an all women panel."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT pm.showid
        FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        WHERE s.bestof = 0 AND s.repeatshowid IS NULL
        AND s.showdate <> '2018-10-27'
        AND p.panelistgender = 'F'
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
