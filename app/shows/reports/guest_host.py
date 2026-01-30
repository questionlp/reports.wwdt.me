# Copyright (c) 2018-2026 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Show Guest Hosts Report Functions."""

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from .show_details import (
    retrieve_show_date_by_id,
    retrieve_show_guests,
    retrieve_show_panelists,
)


def retrieve_shows_guest_host(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict]:
    """Retrieve a list of shows with guest hosts."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT s.showid, s.showdate, s.bestof, s.repeatshowid, h.host,
        h.hostslug, sk.scorekeeper, sk.scorekeeperslug,
        skm.guest as scorekeeper_guest, l.venue, l.city, l.state
        FROM ww_showhostmap hm
        JOIN ww_hosts h ON h.hostid = hm.hostid
        JOIN ww_showskmap skm ON skm.showid = hm.showid
        JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid
        JOIN ww_shows s ON s.showid = hm.showid
        JOIN ww_showlocationmap lm ON lm.showid = hm.showid
        JOIN ww_locations l ON l.locationid = lm.locationid
        WHERE hm.guest = 1
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
                "original_show_date": (
                    retrieve_show_date_by_id(
                        show_id=row["repeatshowid"],
                        database_connection=database_connection,
                    )
                    if row["repeatshowid"]
                    else None
                ),
                "location": {
                    "venue": row["venue"],
                    "city": row["city"],
                    "state": row["state"],
                },
                "host": row["host"],
                "host_slug": row["hostslug"],
                "scorekeeper": row["scorekeeper"],
                "scorekeeper_slug": row["scorekeeperslug"],
                "scorekeeper_guest": bool(row["scorekeeper_guest"]),
                "panelists": retrieve_show_panelists(show_id, database_connection),
                "guests": retrieve_show_guests(show_id, database_connection),
            }
        )

    return shows
