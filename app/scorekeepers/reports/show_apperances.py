# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Scorekeeper Show Appearances Report Functions."""

from typing import Any

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from app.shows.reports.show_details import (
    retrieve_show_date_by_id,
    retrieve_show_guests,
    retrieve_show_panelists_details,
)


def retrieve_appearance_details(
    scorekeeper_slug: str,
    year: int,
    database_connection: MySQLConnection | PooledMySQLConnection,
    include_decimal_scores: bool = False,
) -> list[dict[str, Any]]:
    """Retrieves details for all appearances for a given scorekeeper and year.

    Returned information includes show date, show flags, location, host,
    panelists, and Not My Job guest(s).
    """
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT s.showid, s.showdate, s.bestof, s.repeatshowid,
        l.venue, l.city, l.state, h.host, h.hostslug
        FROM ww_showskmap skm
        JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid
        JOIN ww_shows s ON s.showid = skm.showid
        JOIN ww_showhostmap hm ON hm.showid = skm.showid
        JOIN ww_hosts h ON h.hostid = hm.hostid
        JOIN ww_showlocationmap lm ON lm.showid = skm.showid
        JOIN ww_locations l on l.locationid = lm.locationid
        WHERE sk.scorekeeperslug = %s AND YEAR(s.showdate) = %s
        ORDER BY s.showdate ASC;
    """

    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(
        query,
        (
            scorekeeper_slug,
            year,
        ),
    )
    results = cursor.fetchall()
    cursor.close()

    if not results:
        return None

    _appearances = []
    for row in results:
        _panelists = retrieve_show_panelists_details(
            show_id=row["showid"],
            database_connection=database_connection,
            include_decimal_scores=include_decimal_scores,
        )

        _guests = retrieve_show_guests(
            show_id=row["showid"], database_connection=database_connection
        )

        _show_info = {
            "date": row["showdate"].isoformat(),
            "best_of": bool(row["bestof"]),
            "repeat": bool(row["repeatshowid"]),
            "original_show_date": (
                retrieve_show_date_by_id(
                    show_id=row["repeatshowid"], database_connection=database_connection
                )
                if row["repeatshowid"]
                else None
            ),
            "location": {
                "venue": row["venue"],
                "city": row["city"],
                "state": row["state"],
            },
            "host": {
                "name": row["host"],
                "slug": row["hostslug"],
            },
            "panelists": _panelists,
            "guests": _guests,
        }

        _appearances.append(_show_info)

    return _appearances
