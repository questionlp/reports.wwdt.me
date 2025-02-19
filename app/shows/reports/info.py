# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Show Description and Notes Report Functions."""

from typing import Any

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from .show_details import retrieve_show_date_by_id


def retrieve_show_descriptions(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict[str, Any]]:
    """Returns a list with all shows and their descriptions."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    # Get all shows and descriptions
    query = """
        SELECT s.showid, s.showdate, s.bestof, s.repeatshowid,
        sd.showdescription
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
                "best_of": bool(show["bestof"]),
                "repeat": bool(show["repeatshowid"]),
                "original_show_date": (
                    retrieve_show_date_by_id(
                        show_id=show["repeatshowid"],
                        database_connection=database_connection,
                    )
                    if show["repeatshowid"]
                    else None
                ),
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
        SELECT s.showid, s.showdate, s.bestof, s.repeatshowid,
        sn.shownotes
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
                "best_of": bool(show["bestof"]),
                "repeat": bool(show["repeatshowid"]),
                "original_show_date": (
                    retrieve_show_date_by_id(
                        show_id=show["repeatshowid"],
                        database_connection=database_connection,
                    )
                    if show["repeatshowid"]
                    else None
                ),
                "notes": show["shownotes"],
            }
        )

    return shows
