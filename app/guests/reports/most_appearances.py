# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Guest Most Appearances Report Functions."""

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from app.utility import multi_key_sort


def retrieve_guest_most_appearances_all(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> dict[str, dict]:
    """Returns a dictionary of all guests that have appeared on the show more than once.

    Dictionary keys are ordered by number of appearances in descending
    order, across all shows
    """
    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(dictionary=True)
    query = """
        SELECT g.guestid, g.guest, g.guestslug,
        count(gm.showid) AS appearances
        FROM ww_showguestmap gm
        JOIN ww_guests g ON g.guestid = gm.guestid
        JOIN ww_shows s ON s.showid = gm.showid
        WHERE g.guestslug <> 'none'
        GROUP BY g.guestid
        HAVING count(gm.showid) > 1
        ORDER BY count(gm.showid) DESC;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    database_connection.close()

    if not result:
        return None

    _guests = {}
    for row in result:
        _guests[row["guestid"]] = {
            "id": row["guestid"],
            "name": row["guest"],
            "slug": row["guestslug"],
            "all_shows": row["appearances"],
        }

    return _guests


def retrieve_guest_most_appearances_regular(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> dict[str, dict]:
    """Returns a dictionary of all guests that have appeared on the show more than once.

    Dictionary entries are ordered by number of appearances in descending
    order, across regular shows.
    """
    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(dictionary=True)
    query = """
        SELECT g.guestid, g.guest, g.guestslug,
        count(gm.showid) AS appearances
        FROM ww_showguestmap gm
        JOIN ww_guests g ON g.guestid = gm.guestid
        JOIN ww_shows s ON s.showid = gm.showid
        WHERE g.guestslug <> 'none'
        AND s.bestof = 0 AND s.repeatshowid IS null
        GROUP BY g.guestid;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    database_connection.close()

    if not result:
        return None

    _guests = {}
    for row in result:
        _guests[row["guestid"]] = {
            "id": row["guestid"],
            "name": row["guest"],
            "slug": row["guestslug"],
            "regular_shows": row["appearances"],
        }

    return _guests


def guest_multiple_appearances(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict]:
    """Get a list of guests that have appeared on the show multiple times.

    Appearances includes all shows and regular shows.
    """
    guests_all_shows = retrieve_guest_most_appearances_all(
        database_connection=database_connection
    )
    guests_regular_shows = retrieve_guest_most_appearances_regular(
        database_connection=database_connection
    )

    _guests = []
    for guest in guests_all_shows:
        guest = guests_all_shows[guest]
        guest_id = guest["id"]
        if guest_id in guests_regular_shows:
            guest["regular_shows"] = guests_regular_shows[guest_id]["regular_shows"]
        else:
            guest["regular_shows"] = 0
        _guests.append(guest)

    return multi_key_sort(_guests, ["-all_shows", "-regular_shows", "slug"])
