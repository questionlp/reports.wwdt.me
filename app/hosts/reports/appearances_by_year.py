# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Host Appearances by Year Report Functions."""

from typing import Any

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from app.panelists.reports.appearances_by_year import retrieve_all_years


def retrieve_appearance_counts_by_year(
    year: int, database_connection: MySQLConnection | PooledMySQLConnection
) -> dict[str, dict[str, str | int | None]]:
    """Retrieve host appearance counts for a given year."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT h.hostid, h.host, h.hostslug, COUNT(h.hostid) AS count
        FROM ww_showhostmap hm
        JOIN ww_shows s ON s.showid = hm.showid
        JOIN ww_hosts h ON h.hostid = hm.hostid
        WHERE YEAR(s.showdate) = %s AND s.bestof = 0
        AND s.repeatshowid IS NULL
        GROUP BY h.hostid, h.host, h.hostslug
        ORDER BY COUNT(h.hostid) DESC, h.host ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (year,))
    results = cursor.fetchall()
    cursor.close()

    all_query = """
        SELECT h.hostid, h.host, h.hostslug, COUNT(h.hostid) AS count
        FROM ww_showhostmap hm
        JOIN ww_shows s ON s.showid = hm.showid
        JOIN ww_hosts h ON h.hostid = hm.hostid
        WHERE YEAR(s.showdate) = %s
        GROUP BY h.hostid, h.host, h.hostslug
        ORDER BY COUNT(h.hostid) DESC, h.host ASC;
    """
    all_cursor = database_connection.cursor(dictionary=True)
    all_cursor.execute(all_query, (year,))
    all_results = all_cursor.fetchall()
    all_cursor.close()

    if not results or not all_results:
        return None

    _appearances = {}
    for row in results:
        _appearances[row["hostslug"]] = {
            "name": row["host"],
            "slug": row["hostslug"],
            "regular_appearances": row["count"],
        }

    for row in all_results:
        if row["hostslug"] not in _appearances:
            _appearances[row["hostslug"]] = {
                "name": row["host"],
                "slug": row["hostslug"],
                "regular_appearances": 0,
                "all_appearances": row["count"],
            }
        else:
            _appearances[row["hostslug"]]["all_appearances"] = row["count"]

    return _appearances


def retrieve_host_appearance_counts(
    host_id: int, database_connection: MySQLConnection | PooledMySQLConnection
) -> list[dict[str | int, int]]:
    """Retrieve yearly appearance counts for a given host ID.

    Appearance counts exclude both Best Of and repeat shows.
    """
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT YEAR(s.showdate) AS year, COUNT(h.host) AS count
        FROM ww_showhostmap hm
        JOIN ww_shows s ON s.showid = hm.showid
        JOIN ww_hosts h ON h.hostid = hm.hostid
        WHERE hm.hostid = %s AND s.bestof = 0
        AND s.repeatshowid IS NULL
        GROUP BY h.host, YEAR(s.showdate)
        ORDER BY h.host ASC, YEAR(s.showdate) ASC;
        """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (host_id,))
    results = cursor.fetchall()
    cursor.close()

    if not results:
        return None

    _appearances = {}
    total_appearances = 0
    for row in results:
        _appearances[row["year"]] = row["count"]
        total_appearances += row["count"]

    _appearances["total"] = total_appearances
    return _appearances


def retrieve_host_appearance_counts_all(
    host_id: int, database_connection: MySQLConnection | PooledMySQLConnection
) -> list[dict[str | int, int]]:
    """Retrieve yearly appearance counts for a given host ID.

    Appearance counts include both Best Of and repeat shows.
    """
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT YEAR(s.showdate) AS year, COUNT(h.host) AS count
        FROM ww_showhostmap hm
        JOIN ww_shows s ON s.showid = hm.showid
        JOIN ww_hosts h ON h.hostid = hm.hostid
        WHERE hm.hostid = %s
        GROUP BY h.host, YEAR(s.showdate)
        ORDER BY h.host ASC, YEAR(s.showdate) ASC;
        """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (host_id,))
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    _appearances = {}
    total_appearances = 0
    for row in result:
        _appearances[row["year"]] = row["count"]
        total_appearances += row["count"]

    _appearances["total"] = total_appearances
    return _appearances


def retrieve_all_appearance_counts(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict[str, Any]]:
    """Retrieve all appearance counts for all hosts from the database."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT DISTINCT h.hostid, h.host, h.hostslug
        FROM ww_showhostmap hm
        JOIN ww_hosts h ON h.hostid = hm.hostid
        JOIN ww_shows s ON s.showid = hm.showid
        WHERE s.bestof = 0 AND s.repeatshowid IS NULL
        ORDER BY h.host ASC;
        """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    _hosts = []
    for row in result:
        host_id = row["hostid"]
        _hosts.append(
            {
                "name": row["host"],
                "slug": row["hostslug"],
                "regular_appearances": retrieve_host_appearance_counts(
                    host_id=host_id, database_connection=database_connection
                ),
                "all_appearances": retrieve_host_appearance_counts_all(
                    host_id=host_id, database_connection=database_connection
                ),
            }
        )

    return _hosts


def retrieve_all_appearances_by_year(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> dict[int, dict[str, str | int | None]]:
    """Retrieve all appearance counts for all hosts from the database."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    _years_list = retrieve_all_years(database_connection=database_connection)

    if not _years_list:
        return None

    _years = {}
    for _year in _years_list:
        _appearances = retrieve_appearance_counts_by_year(
            year=_year, database_connection=database_connection
        )

        if _appearances:
            _years[_year] = _appearances
        else:
            _years[_year] = None

    return _years
