# Copyright (c) 2018-2024 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Show Details Report Functions."""
from typing import Any

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection


def retrieve_show_guests(
    show_id: int, database_connection: MySQLConnection | PooledMySQLConnection
) -> list[dict[str, str]]:
    """Retrieve the Not My Job guest for the requested show ID."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT g.guestid, g.guest, g.guestslug
        FROM ww_showguestmap gm
        JOIN ww_guests g on g.guestid = gm.guestid
        WHERE gm.showid = %s;
        """
    cursor = database_connection.cursor(named_tuple=True)
    cursor.execute(query, (show_id,))
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    guests = []
    for row in result:
        guests.append(
            {
                "id": row.guestid,
                "name": row.guest,
                "slug": row.guestslug,
            }
        )

    return guests


def retrieve_show_panelists(
    show_id: int, database_connection: MySQLConnection | PooledMySQLConnection
) -> list[dict[str, str]]:
    """Retrieve panelists for the requested show ID."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT p.panelistid, p.panelist, p.panelistslug
        FROM ww_showpnlmap pm
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        WHERE pm.showid = %s
        ORDER BY pm.showpnlmapid ASC;
        """
    cursor = database_connection.cursor(named_tuple=True)
    cursor.execute(query, (show_id,))
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    panelists = []
    for row in result:
        panelists.append(
            {
                "id": row.panelistid,
                "name": row.panelist,
                "slug": row.panelistslug,
            }
        )

    return panelists


def retrieve_all_shows(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict[str, Any]]:
    """Retrieve a list of all shows and basic information.

    Basic information for each show includes location, host,
    scorekeeper, panelists and guest.
    """
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT s.showid, s.showdate, s.bestof, s.repeatshowid,
        l.venue, l.city, l.state, h.host, sk.scorekeeper
        FROM ww_shows s
        JOIN ww_showlocationmap lm ON lm.showid = s.showid
        JOIN ww_locations l on l.locationid = lm.locationid
        JOIN ww_showhostmap hm ON hm.showid = s.showid
        JOIN ww_hosts h on h.hostid = hm.hostid
        JOIN ww_showskmap skm ON skm.showid = s.showid
        JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid
        AND s.showdate < NOW()
        ORDER BY s.showdate ASC;
        """
    cursor = database_connection.cursor(named_tuple=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    shows = []
    show_count = 1
    for row in result:
        shows.append(
            {
                "count": show_count,
                "id": row.showid,
                "date": row.showdate,
                "best_of": bool(row.bestof),
                "repeat": bool(row.repeatshowid),
                "location": {
                    "venue": row.venue,
                    "city": row.city,
                    "state": row.state,
                },
                "host": row.host,
                "scorekeeper": row.scorekeeper,
                "guests": retrieve_show_guests(
                    show_id=row.showid, database_connection=database_connection
                ),
                "panelists": retrieve_show_panelists(
                    show_id=row.showid, database_connection=database_connection
                ),
            }
        )

        show_count += 1

    return shows


def retrieve_all_original_shows(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict[str, Any]]:
    """Retrieve a list of all original shows and basic information.

    Basic information for each show includes location, host,
    scorekeeper, panelists and guest.
    """
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT s.showid, s.showdate, l.venue, l.city, l.state,
        h.host, sk.scorekeeper
        FROM ww_shows s
        JOIN ww_showlocationmap lm ON lm.showid = s.showid
        JOIN ww_locations l on l.locationid = lm.locationid
        JOIN ww_showhostmap hm ON hm.showid = s.showid
        JOIN ww_hosts h on h.hostid = hm.hostid
        JOIN ww_showskmap skm ON skm.showid = s.showid
        JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid
        WHERE s.bestof = 0 AND s.repeatshowid IS NULL
        AND s.showdate < NOW()
        ORDER BY s.showdate ASC;
        """
    cursor = database_connection.cursor(named_tuple=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    shows = []
    show_count = 1
    for row in result:
        guest = retrieve_show_guests(
            show_id=row.showid, database_connection=database_connection
        )

        show_guest = guest[0] if guest else None

        shows.append(
            {
                "count": show_count,
                "id": row.showid,
                "date": row.showdate,
                "location": {
                    "venue": row.venue,
                    "city": row.city,
                    "state": row.state,
                },
                "host": row.host,
                "scorekeeper": row.scorekeeper,
                "panelists": retrieve_show_panelists(
                    show_id=row.showid, database_connection=database_connection
                ),
                "guest": show_guest,
            }
        )

        show_count += 1

    return shows
