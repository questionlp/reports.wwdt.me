# Copyright (c) 2018-2026 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Host Debut by Year Report Functions."""

from typing import Any

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from app.panelists.reports.appearances import retrieve_panelists_by_show_id
from app.shows.reports.show_details import retrieve_show_date_by_id

from .appearances import retrieve_appearances_by_host


def retrieve_show_years(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[int]:
    """Retrieve a list of all show years."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT DISTINCT YEAR(showdate) AS year
        FROM ww_shows
        ORDER BY YEAR(showdate) ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    return [row["year"] for row in result]


def retrieve_show_info(
    show_date: str, database_connection: MySQLConnection | PooledMySQLConnection
) -> dict[str, Any]:
    """Retrieve show host, scorekeeper and Not My Job guest for the requested show ID."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT s.showid, s.bestof, s.repeatshowid, sk.scorekeeper,
        sk.scorekeeperslug, skm.guest
        FROM ww_showskmap skm
        JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid
        JOIN ww_shows s ON s.showid = skm.showid
        WHERE s.showdate = %s;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (show_date,))
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return None

    return {
        "id": result["showid"],
        "best_of": bool(result["bestof"]),
        "repeat": bool(result["repeatshowid"]),
        "original_show_date": (
            retrieve_show_date_by_id(
                show_id=result["repeatshowid"], database_connection=database_connection
            )
            if result["repeatshowid"]
            else None
        ),
        "scorekeeper": {
            "name": result["scorekeeper"],
            "slug": result["scorekeeperslug"],
            "guest": bool(result["guest"]),
        },
    }


def retrieve_show_guests(
    show_id: int, database_connection: MySQLConnection | PooledMySQLConnection
) -> list[str]:
    """Retrieves a list of Not My Job guest(s) for the requested show ID."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT g.guest
        FROM ww_showguestmap gm
        JOIN ww_guests g ON g.guestid = gm.guestid
        WHERE gm.showid = %s
        AND g.guestid <> 76
        ORDER BY gm.showguestmapid ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (show_id,))
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    return [row["guest"] for row in result]


def retrieve_hosts_first_shows(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> dict[str, Any]:
    """Returns a dictionary containing all panelists and their first shows."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT h.hostid, h.host, h.hostslug, hm.guest,
        MIN(s.showdate) AS first, YEAR(MIN(s.showdate)) AS year
        FROM ww_showhostmap hm
        JOIN ww_hosts h ON h.hostid = hm.hostid
        JOIN ww_shows s ON s.showid = hm.showid
        WHERE h.hostslug <> 'tbd'
        GROUP BY h.hostid, h.hostslug, hm.guest
        ORDER BY MIN(s.showdate) ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    hosts = {}
    for row in result:
        show_info = retrieve_show_info(
            show_date=row["first"], database_connection=database_connection
        )
        appearance_info = retrieve_appearances_by_host(
            host_slug=row["hostslug"], database_connection=database_connection
        )

        hosts[row["hostslug"]] = {
            "id": row["hostid"],
            "host_name": row["host"],
            "host_slug": row["hostslug"],
            "host_guest": bool(row["guest"]),
            "show": row["first"].isoformat(),
            "show_id": show_info["id"],
            "year": row["year"],
            "best_of": show_info["best_of"],
            "repeat": show_info["repeat"],
            "original_show_date": show_info["original_show_date"],
            "regular_appearances": appearance_info["regular"],
            "scorekeeper": show_info["scorekeeper"],
            "panelists": retrieve_panelists_by_show_id(
                show_info["id"], database_connection=database_connection
            ),
            "guests": retrieve_show_guests(
                show_id=show_info["id"], database_connection=database_connection
            ),
        }

    return hosts


def host_debuts_by_year(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> dict[str, Any]:
    """Returns a dictionary of show years with a list of panelists' debut information."""
    show_years = retrieve_show_years(database_connection=database_connection)
    hosts = retrieve_hosts_first_shows(database_connection=database_connection)

    years_debut = {}
    for year in show_years:
        years_debut[year] = []

    for host in hosts:
        host_info = hosts[host]
        years_debut[host_info["year"]].append(host_info)

    return years_debut
