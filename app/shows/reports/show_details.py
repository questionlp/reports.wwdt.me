# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Show Details Report Functions."""

from typing import Any

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection


def retrieve_show_date_by_id(
    show_id: int, database_connection: MySQLConnection | PooledMySQLConnection
) -> str | None:
    """Retrieve a show date for a given show ID."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT showdate FROM ww_shows
        WHERE showid = %s
        LIMIT 1;
    """
    cursor = database_connection.cursor(dictionary=False)
    cursor.execute(query, (show_id,))
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return None

    return result[0].isoformat()


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
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (show_id,))
    results = cursor.fetchall()
    cursor.close()

    if not results:
        return None

    guests = []
    for row in results:
        guests.append(
            {
                "id": row["guestid"],
                "name": row["guest"],
                "slug": row["guestslug"],
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
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (show_id,))
    results = cursor.fetchall()
    cursor.close()

    if not results:
        return None

    panelists = []
    for row in results:
        panelists.append(
            {
                "id": row["panelistid"],
                "name": row["panelist"],
                "slug": row["panelistslug"],
            }
        )

    return panelists


def retrieve_show_panelists_details(
    show_id: int,
    database_connection: MySQLConnection | PooledMySQLConnection,
    include_decimal_scores: bool = False,
) -> list[dict[str, str]]:
    """Retrieve details for panelists for the requested show ID."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    if include_decimal_scores:
        query = """
            SELECT p.panelistid, p.panelist, p.panelistslug,
            pm.panelistlrndstart, pm.panelistlrndstart_decimal,
            pm.panelistlrndcorrect, pm.panelistlrndcorrect_decimal,
            pm.panelistscore, pm.panelistscore_decimal, pm.showpnlrank
            FROM ww_showpnlmap pm
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            WHERE pm.showid = %s
            ORDER BY pm.showpnlmapid ASC;
        """
    else:
        query = """
            SELECT p.panelistid, p.panelist, p.panelistslug,
            pm.panelistlrndstart, pm.panelistlrndcorrect, pm.panelistscore,
            pm.showpnlrank
            FROM ww_showpnlmap pm
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            WHERE pm.showid = %s
            ORDER BY pm.showpnlmapid ASC;
        """

    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (show_id,))
    results = cursor.fetchall()
    cursor.close()

    if not results:
        return None

    panelists = []
    for row in results:
        panelists.append(
            {
                "id": row["panelistid"],
                "name": row["panelist"],
                "slug": row["panelistslug"],
                "scoring": {
                    "start": row["panelistlrndstart"],
                    "start_decimal": (
                        row["panelistlrndstart_decimal"]
                        if include_decimal_scores
                        else None
                    ),
                    "correct": row["panelistlrndcorrect"],
                    "correct_decimal": (
                        row["panelistlrndcorrect_decimal"]
                        if include_decimal_scores
                        else None
                    ),
                    "score": row["panelistscore"],
                    "score_decimal": (
                        row["panelistscore_decimal"] if include_decimal_scores else None
                    ),
                    "rank": row["showpnlrank"],
                },
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
        WHERE s.showdate < NOW()
        ORDER BY s.showdate ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()

    if not results:
        return None

    shows = []
    show_count = 1
    for row in results:
        shows.append(
            {
                "count": show_count,
                "id": row["showid"],
                "date": row["showdate"],
                "best_of": bool(row["bestof"]),
                "repeat": bool(row["repeatshowid"]),
                "original_show_date": (
                    retrieve_show_date_by_id(
                        show_id=row["repeatshowid"],
                        database_connection=database_connection,
                    )
                    if row["repeatshowid"]
                    else None
                ),
                "location": {
                    "venue": row["venue"],
                    "city": row["city"],
                    "state": row["state"],
                },
                "host": row["host"],
                "scorekeeper": row["scorekeeper"],
                "guests": retrieve_show_guests(
                    show_id=row["showid"], database_connection=database_connection
                ),
                "panelists": retrieve_show_panelists(
                    show_id=row["showid"], database_connection=database_connection
                ),
            }
        )

        show_count += 1

    return shows


def retrieve_all_best_of_shows(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict[str, Any]]:
    """Retrieve a list of all Best Of shows and basic information.

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
        WHERE s.showdate < NOW()
        AND s.bestof = 1
        ORDER BY s.showdate ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()

    if not results:
        return None

    shows = []
    show_count = 1
    for row in results:
        shows.append(
            {
                "count": show_count,
                "id": row["showid"],
                "date": row["showdate"],
                "best_of": bool(row["bestof"]),
                "repeat": bool(row["repeatshowid"]),
                "original_show_date": (
                    retrieve_show_date_by_id(
                        show_id=row["repeatshowid"],
                        database_connection=database_connection,
                    )
                    if row["repeatshowid"]
                    else None
                ),
                "location": {
                    "venue": row["venue"],
                    "city": row["city"],
                    "state": row["state"],
                },
                "host": row["host"],
                "scorekeeper": row["scorekeeper"],
                "guests": retrieve_show_guests(
                    show_id=row["showid"], database_connection=database_connection
                ),
                "panelists": retrieve_show_panelists(
                    show_id=row["showid"], database_connection=database_connection
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
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()

    if not results:
        return None

    shows = []
    show_count = 1
    for row in results:
        guest = retrieve_show_guests(
            show_id=row["showid"], database_connection=database_connection
        )

        show_guest = guest[0] if guest else None

        shows.append(
            {
                "count": show_count,
                "id": row["showid"],
                "date": row["showdate"],
                "location": {
                    "venue": row["venue"],
                    "city": row["city"],
                    "state": row["state"],
                },
                "host": row["host"],
                "scorekeeper": row["scorekeeper"],
                "panelists": retrieve_show_panelists(
                    show_id=row["showid"], database_connection=database_connection
                ),
                "guest": show_guest,
            }
        )

        show_count += 1

    return shows


def retrieve_all_repeat_shows(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict[str, Any]]:
    """Retrieve a list of all Repeat shows and basic information.

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
        WHERE s.showdate < NOW()
        AND s.repeatshowid IS NOT NULL
        ORDER BY s.showdate ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()

    if not results:
        return None

    shows = []
    show_count = 1
    for row in results:
        shows.append(
            {
                "count": show_count,
                "id": row["showid"],
                "date": row["showdate"],
                "best_of": bool(row["bestof"]),
                "repeat": bool(row["repeatshowid"]),
                "original_show_date": (
                    retrieve_show_date_by_id(
                        show_id=row["repeatshowid"],
                        database_connection=database_connection,
                    )
                    if row["repeatshowid"]
                    else None
                ),
                "location": {
                    "venue": row["venue"],
                    "city": row["city"],
                    "state": row["state"],
                },
                "host": row["host"],
                "scorekeeper": row["scorekeeper"],
                "guests": retrieve_show_guests(
                    show_id=row["showid"], database_connection=database_connection
                ),
                "panelists": retrieve_show_panelists(
                    show_id=row["showid"], database_connection=database_connection
                ),
            }
        )

        show_count += 1

    return shows


def retrieve_all_repeat_best_of_shows(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict[str, Any]]:
    """Retrieve a list of all Repeat Best Of shows and basic information.

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
        WHERE s.showdate < NOW()
        AND s.bestof = 1 AND s.repeatshowid IS NOT NULL
        ORDER BY s.showdate ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()

    if not results:
        return None

    shows = []
    show_count = 1
    for row in results:
        shows.append(
            {
                "count": show_count,
                "id": row["showid"],
                "date": row["showdate"],
                "best_of": bool(row["bestof"]),
                "repeat": bool(row["repeatshowid"]),
                "original_show_date": (
                    retrieve_show_date_by_id(
                        show_id=row["repeatshowid"],
                        database_connection=database_connection,
                    )
                    if row["repeatshowid"]
                    else None
                ),
                "location": {
                    "venue": row["venue"],
                    "city": row["city"],
                    "state": row["state"],
                },
                "host": row["host"],
                "scorekeeper": row["scorekeeper"],
                "guests": retrieve_show_guests(
                    show_id=row["showid"], database_connection=database_connection
                ),
                "panelists": retrieve_show_panelists(
                    show_id=row["showid"], database_connection=database_connection
                ),
            }
        )

        show_count += 1

    return shows
