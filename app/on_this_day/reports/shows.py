# Copyright (c) 2018-2026 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""On This Day Shows module for Wait Wait Reports."""

from typing import Any

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from app.shows.reports.show_details import (
    retrieve_show_date_by_id,
    retrieve_show_guests,
    retrieve_show_panelists,
)


def retrieve_shows_by_month_day(
    month: int,
    day: int,
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict[str, Any]]:
    """Retrieve show details by a given date."""
    # Simple validation of month and day
    if not 1 <= month <= 12 or not 1 <= day <= 31:
        return None

    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT s.showid, s.showdate, s.bestof, s.repeatshowid, l.venue,
        l.city, l.state, h.host, sk.scorekeeper
        FROM ww_shows s
        JOIN ww_showlocationmap lm ON lm.showid = s.showid
        JOIN ww_locations l ON l.locationid = lm.locationid
        JOIN ww_showhostmap hm ON hm.showid = s.showid
        JOIN ww_hosts h ON h.hostid = hm.hostid
        JOIN ww_showskmap skm ON skm.showid = s.showid
        JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid
        WHERE MONTH(s.showdate) = %s AND DAY(s.showdate) = %s
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(
        query,
        (
            month,
            day,
        ),
    )
    results = cursor.fetchall()
    cursor.close()

    if not results:
        return None

    _shows: list = []
    for row in results:
        _id = row["showid"]
        _shows.append(
            {
                "id": _id,
                "date": row["showdate"].isoformat(),
                "best_of": bool(row["bestof"]),
                "repeat": bool(row["repeatshowid"]),
                "original_show_date": retrieve_show_date_by_id(
                    show_id=row["repeatshowid"], database_connection=database_connection
                )
                if row["repeatshowid"]
                else None,
                "location": {
                    "venue": row["venue"],
                    "city": row["city"],
                    "state": row["state"],
                },
                "host": row["host"],
                "scorekeeper": row["scorekeeper"],
                "panelists": retrieve_show_panelists(
                    show_id=_id, database_connection=database_connection
                ),
                "guests": retrieve_show_guests(
                    show_id=_id, database_connection=database_connection
                ),
            }
        )

    return _shows
