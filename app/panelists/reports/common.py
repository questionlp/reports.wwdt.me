# Copyright (c) 2018-2024 Linh Pham
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
    cursor = database_connection.cursor(named_tuple=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    _panelists = []
    for row in result:
        _panelists.append(
            {
                "id": row.panelistid,
                "slug": row.panelistslug,
                "name": row.panelist,
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
    cursor = database_connection.cursor(named_tuple=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    _panelists = {}
    for row in result:
        _panelists[row.panelistid] = {
            "name": row.panelist,
            "slug": row.panelistslug,
        }

    return _panelists
