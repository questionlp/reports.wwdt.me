# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Common Panelist Report Functions."""

from typing import Any

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection


def retrieve_panelists(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict[str, Any]]:
    """Retrieves a list of all available panelists from the database."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT p.panelistid, p.panelist, p.panelistslug
        FROM ww_panelists p
        WHERE p.panelist <> '<Multiple>'
        ORDER BY p.panelistslug ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    _panelists = []
    for row in result:
        _panelists.append(
            {
                "id": row["panelistid"],
                "slug": row["panelistslug"],
                "name": row["panelist"],
            }
        )

    return _panelists


def retrieve_panelists_by_year(
    year: int,
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict[str, Any]]:
    """Retrieves a list of all available panelists for a given year from the database."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT DISTINCT p.panelistid, p.panelist, p.panelistslug
        FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        WHERE YEAR(s.showdate) = %s
        AND p.panelist <> '<Multiple>'
        ORDER BY p.panelistslug ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (year,))
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    _panelists = []
    for row in result:
        _panelists.append(
            {
                "id": row["panelistid"],
                "slug": row["panelistslug"],
                "name": row["panelist"],
            }
        )

    return _panelists


def retrieve_panelists_id_key(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> dict[int, dict]:
    """Retrieves a dictionary of all available panelists from the database."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT p.panelistid, p.panelist, p.panelistslug
        FROM ww_panelists p
        WHERE p.panelist <> '<Multiple>'
        ORDER BY p.panelistslug ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    _panelists = {}
    for row in result:
        _panelists[row["panelistid"]] = {
            "name": row["panelist"],
            "slug": row["panelistslug"],
        }

    return _panelists


def retrieve_panelist_info_by_slug(
    panelist_slug: str, database_connection: MySQLConnection | PooledMySQLConnection
) -> dict[str, str | int]:
    """Retrieves panelist information for a given panelist slug string."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT p.panelist, p.panelistslug
        FROM ww_panelists p
        WHERE p.panelistslug = %s
        LIMIT 1;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (panelist_slug,))
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return None

    return {"name": result["panelist"], "slug": result["panelistslug"]}
