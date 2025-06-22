# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Host Show Appearances Report Functions."""

from typing import Any

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from app.shows.reports.show_details import (
    retrieve_show_date_by_id,
    retrieve_show_guests,
    retrieve_show_panelists_details,
)

from .debut_by_year import retrieve_show_years


def retrieve_appearance_details_by_year(
    host_slug: str,
    year: int,
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict[str, Any]]:
    """Retrieves details for all appearances for a given host and year.

    Returned information includes show date, show flags, location,
    scorekeeper, panelists, and Not My Job guest(s).
    """
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT s.showid, s.showdate, s.bestof, s.repeatshowid,
        l.venue, l.city, l.state, sk.scorekeeper, sk.scorekeeperslug,
        skm.guest
        FROM ww_showhostmap hm
        JOIN ww_hosts h ON h.hostid = hm.hostid
        JOIN ww_shows s ON s.showid = hm.showid
        JOIN ww_showskmap skm ON skm.showid = hm.showid
        JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid
        JOIN ww_showlocationmap lm ON lm.showid = hm.showid
        JOIN ww_locations l on l.locationid = lm.locationid
        WHERE h.hostslug = %s AND YEAR(s.showdate) = %s
        ORDER BY s.showdate ASC;
    """

    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(
        query,
        (
            host_slug,
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
            "scorekeeper": {
                "name": row["scorekeeper"],
                "slug": row["scorekeeperslug"],
                "guest": bool(row["guest"]),
            },
            "panelists": _panelists,
            "guests": _guests,
        }

        _appearances.append(_show_info)

    return _appearances


def retrieve_appearance_details(
    host_slug: str, database_connection: MySQLConnection | PooledMySQLConnection
) -> dict[int, list[dict[str, Any]]]:
    """Retrieves details for all appearances for a given host for all available years.

    Returned information includes show date, show flags, location,
    scorekeeper, panelists, and Not My Job guest(s).
    """
    if not database_connection.is_connected():
        database_connection.reconnect()

    _years = retrieve_show_years(database_connection=database_connection)
    if not _years:
        return None

    _appearances = {}
    for _year in _years:
        _appearances[_year] = retrieve_appearance_details_by_year(
            host_slug=host_slug, year=_year, database_connection=database_connection
        )

    return _appearances
