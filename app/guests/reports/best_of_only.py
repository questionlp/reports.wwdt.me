# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Guest Best Of Only Appearances Report Functions"""
from typing import Dict, List

import mysql.connector


def retrieve_guest_appearances(
    guest_id: int, database_connection: mysql.connector.connect
) -> List[Dict]:
    """Retrieve a list of shows in which the requested Not My Job guest
    has made an appearance on (including Best Of and Repeats)"""

    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT s.showid, s.showdate, s.bestof, s.repeatshowid, "
        "gm.guestscore, gm.exception "
        "FROM ww_showguestmap gm "
        "JOIN ww_shows s ON s.showid = gm.showid "
        "JOIN ww_guests g ON g.guestid = gm.guestid "
        "WHERE g.guestid = %s "
        "ORDER BY s.showdate ASC;"
    )
    cursor.execute(query, (guest_id,))
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    shows = []
    for row in result:
        shows.append(
            {
                "id": row.showid,
                "date": row.showdate.isoformat(),
                "best_of": bool(row.bestof),
                "repeat_show": bool(row.repeatshowid),
                "score": row.guestscore,
                "exception": bool(row.exception),
            }
        )

    return shows


def retrieve_best_of_only_guests(
    database_connection: mysql.connector.connect,
) -> List[Dict]:
    """Retrieves a list of Not My Job guests that have only appeared
    on Best Of shows"""

    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT DISTINCT g.guestid, g.guest, g.guestslug "
        "FROM ww_showguestmap gm "
        "JOIN ww_shows s ON s.showid = gm.showid "
        "JOIN ww_guests g ON g.guestid = gm.guestid "
        "WHERE s.bestof = 1 AND s.repeatshowid IS NULL "
        "AND g.guestid NOT IN ( "
        "  SELECT gm.guestid "
        "  FROM ww_showguestmap gm "
        "  JOIN ww_shows s ON s.showid = gm.showid "
        "  WHERE s.bestof = 0 AND s.repeatshowid IS NULL )"
    )
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        database_connection.close()
        return None

    guests = []
    for row in result:
        guests.append(
            {
                "id": row.guestid,
                "name": row.guest,
                "slug": row.guestslug,
                "appearances": retrieve_guest_appearances(
                    guest_id=row.guestid, database_connection=database_connection
                ),
            }
        )

    return guests
