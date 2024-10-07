# Copyright (c) 2018-2024 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Show Guest Scorekeeper Report Functions."""
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from app.shows.reports import show_details


def retrieve_shows_guest_scorekeeper(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict]:
    """Retrieve a list of shows with guest scorekeepers."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT s.showid, s.showdate, s.bestof, s.repeatshowid, h.host,
        h.hostslug, hm.guest AS host_guest, sk.scorekeeper,
        sk.scorekeeperslug, l.venue, l.city, l.state
        FROM ww_showhostmap hm
        JOIN ww_hosts h ON h.hostid = hm.hostid
        JOIN ww_showskmap skm ON skm.showid = hm.showid
        JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid
        JOIN ww_shows s ON s.showid = hm.showid
        JOIN ww_showlocationmap lm ON lm.showid = hm.showid
        JOIN ww_locations l ON l.locationid = lm.locationid
        WHERE skm.guest = 1
        ORDER BY s.showdate ASC;
        """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()

    if not result:
        return None

    shows = []
    for row in result:
        show_id = row["showid"]
        shows.append(
            {
                "date": row["showdate"].isoformat(),
                "best_of": bool(row["bestof"]),
                "repeat": bool(row["repeatshowid"]),
                "location": {
                    "venue": row["venue"],
                    "city": row["city"],
                    "state": row["state"],
                },
                "host": row["host"],
                "host_slug": row["hostslug"],
                "host_guest": bool(row["host_guest"]),
                "scorekeeper": row["scorekeeper"],
                "scorekeeper_slug": row["scorekeeperslug"],
                "panelists": show_details.retrieve_show_panelists(
                    show_id, database_connection
                ),
                "guests": show_details.retrieve_show_guests(
                    show_id, database_connection
                ),
            }
        )

    return shows
