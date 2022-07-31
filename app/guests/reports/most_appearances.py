# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Guest Most Appearances Report Functions"""
from typing import Dict, List

import mysql.connector

from app.utility import multi_key_sort


def retrieve_guest_most_appearances_all(
    database_connection: mysql.connector.connect,
) -> Dict[str, Dict]:
    """Returns a dictionary of all guests that have appeared on the
    show more than once, ordered by number of appearances in descending
    order, across all shows"""

    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT g.guestid, g.guest, g.guestslug, "
        "count(gm.showid) AS appearances "
        "FROM ww_showguestmap gm "
        "JOIN ww_guests g ON g.guestid = gm.guestid "
        "JOIN ww_shows s ON s.showid = gm.showid "
        "WHERE g.guest != '[None]' "
        "GROUP BY g.guestid "
        "HAVING count(gm.showid) > 1 "
        "ORDER BY count(gm.showid) DESC;"
    )
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    database_connection.close()

    if not result:
        return None

    _guests = {}
    for row in result:
        _guests[row.guestid] = {
            "id": row.guestid,
            "name": row.guest,
            "slug": row.guestslug,
            "all_shows": row.appearances,
        }

    return _guests


def retrieve_guest_most_appearances_regular(
    database_connection: mysql.connector.connect,
) -> Dict[str, Dict]:
    """Returns a dictionary of all guests that have appeared on the
    show more than once, ordered by number of appearances in descending
    order, across regular shows"""

    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT g.guestid, g.guest, g.guestslug, "
        "count(gm.showid) AS appearances "
        "FROM ww_showguestmap gm "
        "JOIN ww_guests g ON g.guestid = gm.guestid "
        "JOIN ww_shows s ON s.showid = gm.showid "
        "WHERE g.guest != '[None]' "
        "AND s.bestof = 0 AND s.repeatshowid IS null "
        "GROUP BY g.guestid;"
    )
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    database_connection.close()

    if not result:
        return None

    _guests = {}
    for row in result:
        _guests[row.guestid] = {
            "id": row.guestid,
            "name": row.guest,
            "slug": row.guestslug,
            "regular_shows": row.appearances,
        }

    return _guests


def guest_multiple_appearances(
    database_connection: mysql.connector.connect,
) -> List[Dict]:
    """Get a list of guests that have appeared on the show multiple
    times on all shows and regular shows"""

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
