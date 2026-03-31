# Copyright (c) 2018-2026 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Guest Scores Report Functions."""

from typing import Any

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from app.shows.reports.show_details import retrieve_show_date_by_id
from app.utility import multi_key_sort


def retrieve_all_scoring_exceptions(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict[str, Any]]:
    """Retrieve a list of all Not My Job scoring exceptions."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(dictionary=True)
    query = """
        SELECT s.showdate, g.guestid, g.guest, g.guestslug,
        gm.guestscore, gm.exception, sn.shownotes
        FROM ww_showguestmap gm
        JOIN ww_shows s ON s.showid = gm.showid
        JOIN ww_guests g ON g.guestid = gm.guestid
        JOIN ww_shownotes sn ON sn.showid = gm.showid
        WHERE s.bestof = 0 AND s.repeatshowid IS NULL
        AND gm.exception = 1
        ORDER BY s.showdate ASC;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    cursor = database_connection.cursor(dictionary=True)
    best_of_only_query = """
        SELECT s.showdate, g.guestid, g.guest, g.guestslug,
        gm.guestscore, gm.exception, sn.shownotes
        FROM ww_showguestmap gm
        JOIN ww_shows s ON s.showid = gm.showid
        JOIN ww_guests g ON g.guestid = gm.guestid
        JOIN ww_shownotes sn ON sn.showid = gm.showid
        WHERE s.bestof = 1 AND s.repeatshowid IS NULL
        AND g.guestid NOT IN (
            SELECT gm.guestid
            FROM ww_showguestmap gm
            JOIN ww_shows s ON s.showid = gm.showid
            WHERE s.bestof = 0 AND s.repeatshowid IS NULL
        )
        AND gm.exception = 1
        ORDER BY s.showdate ASC;
    """
    cursor.execute(best_of_only_query)
    result_best_of_only = cursor.fetchall()
    cursor.close()

    if not result and not result_best_of_only:
        return None

    _exceptions = []
    for row in result:
        _exceptions.append(
            {
                "id": row["guestid"],
                "name": row["guest"],
                "slug": row["guestslug"],
                "show_date": row["showdate"],
                "score": row["guestscore"],
                "exception": bool(row["exception"]),
                "notes": row["shownotes"],
            }
        )

    if result_best_of_only:
        for row in result_best_of_only:
            _exceptions.append(
                {
                    "id": row["guestid"],
                    "name": row["guest"],
                    "slug": row["guestslug"],
                    "show_date": row["showdate"],
                    "score": row["guestscore"],
                    "exception": bool(row["exception"]),
                    "notes": row["shownotes"],
                }
            )

    _sorted_exceptions = multi_key_sort(
        items=_exceptions, columns=["show_date", "name"]
    )
    return _sorted_exceptions


def retrieve_all_three_pointers(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict]:
    """Retrieve a list instances where Not My Job guests have won.

    This includes instances where a guest has answered all three questions
    correct or received all three points.
    """
    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(dictionary=True)
    query = """
        (
            SELECT g.guestid, g.guest, g.guestslug, s.showid, s.showdate,
            gm.guestscore, gm.exception, sk.scorekeeperid, sk.scorekeeper,
            sk.scorekeeperslug, skm.guest AS scorekeeper_guest, sn.shownotes
            FROM ww_showguestmap gm
            JOIN ww_shows s ON s.showid = gm.showid
            JOIN ww_guests g ON g.guestid = gm.guestid
            JOIN ww_shownotes sn ON sn.showid = gm.showid
            JOIN ww_showskmap skm ON skm.showid = gm.showid
            JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid
            WHERE s.bestof = 0 AND s.repeatshowid IS NULL
            AND gm.guestscore = 3
        )
        UNION
        (
            SELECT g.guestid, g.guest, g.guestslug, s.showid, s.showdate,
            gm.guestscore, gm.exception, sk.scorekeeperid, sk.scorekeeper,
            sk.scorekeeperslug, skm.guest AS scorekeeper_guest, sn.shownotes
            FROM ww_showguestmap gm
            JOIN ww_shows s ON s.showid = gm.showid
            JOIN ww_guests g ON g.guestid = gm.guestid
            JOIN ww_shownotes sn ON sn.showid = gm.showid
            JOIN ww_showskmap skm ON skm.showid = gm.showid
            JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid
            WHERE s.bestof = 1 AND s.repeatshowid IS NULL
            AND gm.guestscore = 3
            AND g.guestid NOT IN (
            SELECT gm.guestid
            FROM ww_showguestmap gm
            JOIN ww_shows s ON s.showid = gm.showid
            WHERE s.bestof = 0 AND s.repeatshowid IS NULL
            )
        )
        ORDER BY guest ASC, showdate ASC;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    three_pointers = []
    for row in result:
        three_pointers.append(
            {
                "id": row["guestid"],
                "name": row["guest"],
                "slug": row["guestslug"],
                "show_date": row["showdate"].isoformat(),
                "scorekeeper": {
                    "name": row["scorekeeper"],
                    "slug": row["scorekeeperslug"],
                    "guest": bool(row["scorekeeper_guest"]),
                },
                "score": row["guestscore"],
                "exception": bool(row["exception"]),
                "show_notes": row["shownotes"],
            }
        )

    return three_pointers


def retrieve_all_missing_scores(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict[str, str | int | bool | None]]:
    """Retrieve all Not My Job guests with no scores entered."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT s.showdate, s.bestof, s.repeatshowid, g.guest,
        g.guestslug, gm.guestscore, gm.exception
        FROM ww_showguestmap gm
        JOIN ww_guests g ON g.guestid = gm.guestid
        JOIN ww_shows s ON s.showid = gm.showid
        WHERE gm.guestscore IS NULL
        AND g.guestslug <> 'none'
        AND s.showdate < NOW()
        ORDER BY s.showdate ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()

    if not results:
        return None

    _guests = []
    for row in results:
        _guests.append(
            {
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
                "name": row["guest"],
                "slug": row["guestslug"],
                "score": row["guestscore"],
                "exception": bool(row["exception"]),
            }
        )

    return _guests
