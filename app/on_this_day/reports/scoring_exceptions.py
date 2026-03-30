# Copyright (c) 2018-2026 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""On This Day Guest Scoring Exceptions module for Wait Wait Reports."""

from typing import Any

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from app.utility import multi_key_sort


def retrieve_scoring_exceptions_by_month_day(
    month: int, day: int, database_connection: MySQLConnection | PooledMySQLConnection
):
    """Retrieve Not My Job guest scoring exceptions for a given month and day."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(dictionary=True)
    query = """
        SELECT g.guest, g.guestslug, s.showdate, gm.guestscore, gm.exception
        FROM ww_showguestmap gm
        JOIN ww_shows s ON s.showid = gm.showid
        JOIN ww_guests g ON g.guestid = gm.guestid
        WHERE MONTH(s.showdate) = %s AND DAY(s.showdate) = %s
        AND s.bestof = 0 AND s.repeatshowid IS NULL
        AND gm.exception = 1
        ORDER BY s.showdate ASC;
    """
    cursor.execute(
        query,
        (
            month,
            day,
        ),
    )
    result = cursor.fetchall()
    cursor.close()

    cursor = database_connection.cursor(dictionary=True)
    best_of_only_query = """
        SELECT s.showdate, g.guest, g.guestslug, gm.guestscore
        FROM ww_showguestmap gm
        JOIN ww_shows s ON s.showid = gm.showid
        JOIN ww_guests g ON g.guestid = gm.guestid
        WHERE MONTH(s.showdate) = %s AND DAY(s.showdate) = %s
        AND g.guestid NOT IN (
            SELECT gm.guestid
            FROM ww_showguestmap gm
            JOIN ww_shows s ON s.showid = gm.showid
            WHERE s.bestof = 0 AND s.repeatshowid IS NULL
        )
        AND s.bestof = 1 AND s.repeatshowid IS NULL
        AND gm.exception = 1
        ORDER BY s.showdate ASC;
    """
    cursor.execute(
        best_of_only_query,
        (
            month,
            day,
        ),
    )
    result_best_of_only = cursor.fetchall()
    cursor.close()

    if not result and not result_best_of_only:
        return None

    _score_exceptions = []
    for row in result:
        _score_exceptions.append(
            {
                "show_date": row["showdate"].isoformat(),
                "name": row["guest"],
                "slug": row["guestslug"],
                "score": row["guestscore"],
            }
        )

    if result_best_of_only:
        for row in result_best_of_only:
            _score_exceptions.append(
                {
                    "show_date": row["showdate"].isoformat(),
                    "name": row["guest"],
                    "slug": row["guestslug"],
                    "score": row["guestscore"],
                }
            )

    _sorted_score_exceptions = multi_key_sort(
        items=_score_exceptions, columns=["show_date", "name"]
    )
    return _sorted_score_exceptions
