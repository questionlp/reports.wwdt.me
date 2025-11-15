# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Hosts Appearances Report Functions."""

from typing import Any

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection


def retrieve_hosts(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict[str, str]]:
    """Retrieves a list of all available hosts from the database."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(dictionary=True)
    query = """
        SELECT h.hostid, h.host, h.hostslug
        FROM ww_hosts h
        WHERE h.hostslug <> 'tbd'
        ORDER BY h.hostslug ASC;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    _hosts = []
    for row in result:
        _hosts.append(
            {
                "name": row["host"],
                "slug": row["hostslug"],
            }
        )

    return _hosts


def retrieve_appearances_by_host(
    host_slug: str, database_connection: MySQLConnection | PooledMySQLConnection
) -> dict[str, int]:
    """Retrieve appearance data for the requested host."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(dictionary=True)
    query = """
        SELECT (
        SELECT COUNT(hm.showid) FROM ww_showhostmap hm
        JOIN ww_shows s ON s.showid = hm.showid
        JOIN ww_hosts h ON h.hostid = hm.hostid
        WHERE s.bestof = 0 AND s.repeatshowid IS NULL AND
        h.hostslug = %s ) AS regular, (
        SELECT COUNT(hm.showid) FROM ww_showhostmap hm
        JOIN ww_shows s ON s.showid = hm.showid
        JOIN ww_hosts h ON h.hostid = hm.hostid
        WHERE h.hostslug = %s ) AS allshows;
    """
    cursor.execute(
        query,
        (
            host_slug,
            host_slug,
        ),
    )
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return {
            "regular": None,
            "all": None,
        }

    return {
        "regular": result["regular"],
        "all": result["allshows"],
    }


def retrieve_first_most_recent_appearances(
    host_slug: str, database_connection: MySQLConnection | PooledMySQLConnection
) -> dict[str, str]:
    """Retrieve first and most recent appearances for both regular and all shows for a host."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(dictionary=True)
    query = """
        SELECT MIN(s.showdate) AS min, MAX(s.showdate) AS max
        FROM ww_showhostmap hm
        JOIN ww_shows s ON s.showid = hm.showid
        JOIN ww_hosts h ON h.hostid = hm.hostid
        WHERE h.hostslug = %s
        AND s.bestof = 0
        AND s.repeatshowid IS null;
    """
    cursor.execute(query, (host_slug,))
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return None

    first = result["min"].isoformat() if result["min"] else None
    most_recent = result["max"].isoformat() if result["max"] else None

    cursor = database_connection.cursor(dictionary=True)
    query = """
        SELECT MIN(s.showdate) AS min, MAX(s.showdate) AS max
        FROM ww_showhostmap hm
        JOIN ww_shows s ON s.showid = hm.showid
        JOIN ww_hosts h ON h.hostid = hm.hostid
        WHERE h.hostslug = %s;
    """
    cursor.execute(query, (host_slug,))
    result_all = cursor.fetchone()
    cursor.close()

    if not result_all:
        return {
            "first": first,
            "most_recent": most_recent,
            "first_all": None,
            "most_recent_all": None,
        }

    first_all = result_all["min"].isoformat() if result_all["min"] else None
    most_recent_all = result_all["max"].isoformat() if result_all["max"] else None

    return {
        "first": first,
        "most_recent": most_recent,
        "first_all": first_all,
        "most_recent_all": most_recent_all,
    }


def retrieve_appearance_summaries(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict[str, Any]]:
    """Retrieve host appearance summary.

    Returned summary includes appearance counts, appearances.
    """
    _hosts = retrieve_hosts(database_connection=database_connection)

    if not _hosts:
        return None

    hosts_summary = {}
    for host in _hosts:
        appearance_count = retrieve_appearances_by_host(
            host_slug=host["slug"], database_connection=database_connection
        )
        first_most_recent = retrieve_first_most_recent_appearances(
            host_slug=host["slug"], database_connection=database_connection
        )

        if appearance_count and first_most_recent:
            hosts_summary[host["slug"]] = {
                "slug": host["slug"],
                "name": host["name"],
                "regular_shows": appearance_count["regular"],
                "all_shows": appearance_count["all"],
                "first": first_most_recent["first"],
                "first_all": first_most_recent["first_all"],
                "most_recent": first_most_recent["most_recent"],
                "most_recent_all": first_most_recent["most_recent_all"],
            }

    return hosts_summary
