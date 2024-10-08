# Copyright (c) 2018-2024 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Show Description and Notes Report Functions."""
from typing import Any

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection


def retrieve_show_descriptions(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict[str, Any]]:
    """Returns a list with all shows and their descriptions."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    # Get all shows and descriptions
    query = """
        SELECT s.showid, s.showdate, sd.showdescription
        FROM ww_showdescriptions sd
        JOIN ww_shows s ON s.showid = sd.showid
        ORDER BY s.showdate;
        """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    shows = []
    for show in result:
        shows.append(
            {
                "id": show["showid"],
                "date": show["showdate"],
                "description": show["showdescription"],
            }
        )

    return shows


def retrieve_show_notes(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict[str, Any]]:
    """Returns a list with all shows and their notes."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    # Get all shows and descriptions
    query = """
        SELECT s.showid, s.showdate, sn.shownotes
        FROM ww_shownotes sn
        JOIN ww_shows s ON s.showid = sn.showid
        ORDER BY s.showdate;
        """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    shows = []
    for show in result:
        shows.append(
            {
                "id": show["showid"],
                "date": show["showdate"],
                "notes": show["shownotes"],
            }
        )

    return shows
