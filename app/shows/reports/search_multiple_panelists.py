# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Search Shows by Multiple Selected Panelists Report Functions."""

from typing import Any

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from . import show_details as details


def retrieve_panelists(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> dict[str, str]:
    """Returns a dictionary containing valid panelists."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT panelistslug, panelist FROM ww_panelists
        WHERE panelistslug <> 'multiple'
        ORDER BY panelist ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    return {row["panelistslug"]: row["panelist"] for row in result}


def retrieve_details(
    show_id: int, database_connection: MySQLConnection | PooledMySQLConnection
) -> list[dict[str, Any]]:
    """Retrieve show details for the requested show ID."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT s.showid, s.showdate, s.bestof, s.repeatshowid, l.venue,
        l.city, l.state, h.host, sk.scorekeeper
        FROM ww_shows s
        JOIN ww_showlocationmap lm ON lm.showid = s.showid
        JOIN ww_locations l on l.locationid = lm.locationid
        JOIN ww_showhostmap hm ON hm.showid = s.showid
        JOIN ww_hosts h on h.hostid = hm.hostid
        JOIN ww_showskmap skm ON skm.showid = s.showid
        JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid
        WHERE s.showid = %s;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (show_id,))
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return None

    return {
        "id": result["showid"],
        "date": result["showdate"].isoformat(),
        "best_of": bool(result["bestof"]),
        "repeat": bool(result["repeatshowid"]),
        "original_show_date": details.retrieve_show_date_by_id(
            show_id=result["repeatshowid"], database_connection=database_connection
        ),
        "location": {
            "venue": result["venue"],
            "city": result["city"],
            "state": result["state"],
        },
        "host": result["host"],
        "scorekeeper": result["scorekeeper"],
        "panelists": details.retrieve_show_panelists(
            show_id=result["showid"], database_connection=database_connection
        ),
        "guests": details.retrieve_show_guests(
            show_id=result["showid"], database_connection=database_connection
        ),
    }


def retrieve_matching_one(
    database_connection: MySQLConnection | PooledMySQLConnection,
    panelist_slug_1: str,
    include_best_of: bool = False,
    include_repeats: bool = False,
) -> list[dict[str, Any]]:
    """Retrieve show details for shows with a panel containing one of the requested panelists."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT s.showid, s.bestof, s.repeatshowid
        FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        WHERE p.panelistslug = %s
        GROUP BY s.showid
        HAVING COUNT(s.showid) = 1
        ORDER BY s.showdate ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (panelist_slug_1,))
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    shows = []
    for row in result:
        best_of = bool(row["bestof"])
        repeat = bool(row["repeatshowid"])

        if (best_of and repeat) and (include_best_of or include_repeats):
            shows.append(
                retrieve_details(
                    show_id=row["showid"], database_connection=database_connection
                )
            )

        if (best_of and not include_best_of) or (repeat and not include_repeats):
            continue

        shows.append(
            retrieve_details(
                show_id=row["showid"], database_connection=database_connection
            )
        )

    return shows


def retrieve_matching_two(
    database_connection: MySQLConnection | PooledMySQLConnection,
    panelist_slug_1: str,
    panelist_slug_2: str,
    include_best_of: bool = False,
    include_repeats: bool = False,
) -> list[dict[str, Any]]:
    """Retrieve show details for shows with a panel containing two of the requested panelists."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT s.showid, s.bestof, s.repeatshowid
        FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        WHERE p.panelistslug IN (%s, %s)
        GROUP BY s.showid
        HAVING COUNT(s.showid) = 2
        ORDER BY s.showdate ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(
        query,
        (
            panelist_slug_1,
            panelist_slug_2,
        ),
    )
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    shows = []
    for row in result:
        best_of = bool(row["bestof"])
        repeat = bool(row["repeatshowid"])

        if (best_of and repeat) and (include_best_of or include_repeats):
            shows.append(
                retrieve_details(
                    show_id=row["showid"], database_connection=database_connection
                )
            )

        if (best_of and not include_best_of) or (repeat and not include_repeats):
            continue

        shows.append(
            retrieve_details(
                show_id=row["showid"], database_connection=database_connection
            )
        )

    return shows


def retrieve_matching_three(
    database_connection: MySQLConnection | PooledMySQLConnection,
    panelist_slug_1: str,
    panelist_slug_2: str,
    panelist_slug_3: str,
    include_best_of: bool = False,
    include_repeats: bool = False,
) -> list[dict[str, Any]]:
    """Retrieve show details for shows with a panel containing three of the requested panelists."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT s.showid, s.bestof, s.repeatshowid
        FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        WHERE p.panelistslug IN (%s, %s, %s)
        GROUP BY s.showid
        HAVING COUNT(s.showid) = 3
        ORDER BY s.showdate ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(
        query,
        (
            panelist_slug_1,
            panelist_slug_2,
            panelist_slug_3,
        ),
    )
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    shows = []
    for row in result:
        best_of = bool(row["bestof"])
        repeat = bool(row["repeatshowid"])

        if (best_of and repeat) and (include_best_of or include_repeats):
            shows.append(
                retrieve_details(
                    show_id=row["showid"], database_connection=database_connection
                )
            )

        if (best_of and not include_best_of) or (repeat and not include_repeats):
            continue

        shows.append(
            retrieve_details(
                show_id=row["showid"], database_connection=database_connection
            )
        )

    return shows
