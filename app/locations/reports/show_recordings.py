# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Location Show Recordings Report Functions."""

from typing import Any

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from app.hosts.reports.debut_by_year import retrieve_show_years
from app.shows.reports.show_details import (
    retrieve_show_date_by_id,
    retrieve_show_guests,
    retrieve_show_panelists_details,
)


def retrieve_recording_details_by_year(
    location_slug: str,
    year: int,
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict[str, Any]]:
    """Retrieves details for all recordings for a given location and year.

    Returned information includes show date, show flags, host,
    scorekeeper, panelists, and Not My Job guest(s).
    """
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT s.showid, s.showdate, s.bestof, s.repeatshowid,
        h.host, h.hostslug, sk.scorekeeper, sk.scorekeeperslug,
        skm.guest
        FROM ww_showlocationmap lm
        JOIN ww_locations l ON l.locationid = lm.locationid
        JOIN ww_shows s ON s.showid = lm.showid
        JOIN ww_showhostmap hm ON hm.showid = lm.showid
        JOIN ww_hosts h ON h.hostid = hm.hostid
        JOIN ww_showskmap skm ON skm.showid = lm.showid
        JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid
        WHERE l.locationslug = %s and YEAR(s.showdate) = %s
        ORDER BY s.showdate ASC;
    """

    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(
        query,
        (
            location_slug,
            year,
        ),
    )
    results = cursor.fetchall()
    cursor.close()

    if not results:
        return None

    _recordings = []
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
            "host": {
                "name": row["host"],
                "slug": row["hostslug"],
            },
            "scorekeeper": {
                "name": row["scorekeeper"],
                "slug": row["scorekeeperslug"],
                "guest": row["guest"],
            },
            "panelists": _panelists,
            "guests": _guests,
        }

        _recordings.append(_show_info)

    return _recordings


def retrieve_recording_details(
    location_slug: str, database_connection: MySQLConnection | PooledMySQLConnection
) -> dict[int, list[dict[str, Any]]]:
    """Retrieves details for all recordings for a given location and all available years.

    Returned information includes show date, show flags, host,
    scorekeeper, panelists, and Not My Job guest(s).
    """
    if not database_connection.is_connected():
        database_connection.reconnect()

    _years = retrieve_show_years(database_connection=database_connection)
    if not _years:
        return None

    _recordings = {}
    for _year in _years:
        _recordings[_year] = retrieve_recording_details_by_year(
            location_slug=location_slug,
            year=_year,
            database_connection=database_connection,
        )

    return _recordings


def retrieve_locations(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict[str, str | None]]:
    """Retrieve a list of locations along with their details."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT l.venue, l.city, l.state, l.locationslug
        FROM ww_locations l
        WHERE locationslug <> 'tbd'
        ORDER BY locationslug ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()

    if not results:
        return None

    _locations = []
    for row in results:
        _location = {
            "venue": row["venue"],
            "city": row["city"],
            "state": row["state"],
            "slug": row["locationslug"],
        }

        if row["venue"] and row["city"] and row["state"]:
            _location["display_name"] = (
                f"{row['venue']} ({row['city']}, {row['state']})"
            )
        elif row["venue"] and (not row["city"] or not row["state"]):
            _location["display_name"] = row["venue"]
        elif row["city"] and row["state"]:
            _location["display_name"] = f"({row['city']}, {row['state']})"
        elif row["city"]:
            _location["display_name"] = row["city"]
        else:
            _location["display_name"] = row["locationslug"]

        _locations.append(_location)

    return _locations


def retrieve_location(
    location_slug: str,
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> dict[str, str | None]:
    """Retrieve details for a given location slug."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT l.venue, l.city, l.state, l.locationslug
        FROM ww_locations l
        WHERE locationslug = %s
        LIMIT 1;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (location_slug,))
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return None

    _location = {
        "venue": result["venue"],
        "city": result["city"],
        "state": result["state"],
        "slug": result["locationslug"],
    }

    if result["venue"] and result["city"] and result["state"]:
        _location["display_name"] = (
            f"{result['venue']} ({result['city']}, {result['state']})"
        )
    elif result["venue"] and (not result["city"] or not result["state"]):
        _location["display_name"] = result["venue"]
    elif result["city"] and result["state"]:
        _location["display_name"] = f"({result['city']}, {result['state']})"
    elif result["city"]:
        _location["display_name"] = result["city"]
    else:
        _location["display_name"] = result["locationslug"]

    return _location
