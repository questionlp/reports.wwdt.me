# Copyright (c) 2018-2026 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Guest Wins by Year Report Functions."""

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from app.shows.reports.show_details import retrieve_show_date_by_id


def retrieve_wins_by_year(
    year: int, database_connection: MySQLConnection | PooledMySQLConnection
) -> list[dict[str, str | int | bool | None]]:
    """Retrieve Not My Job guest wins for a given year.

    Results only include guests that have appeared on regular shows and
    unique guests who have only appeared on Best Of shows.
    """
    if not database_connection.is_connected():
        database_connection.reconnect()

    # Add exclusion of 1998-05-02 due to a scoring exception was made
    # but not a win was not granted
    query = """
        SELECT s.showid, s.showdate, s.bestof, s.repeatshowid, g.guest,
        g.guestslug, gm.guestscore, gm.exception
        FROM ww_showguestmap gm
        JOIN ww_shows s ON s.showid = gm.showid
        JOIN ww_guests g ON g.guestid = gm.guestid
        WHERE gm.showguestmapid IN (
            SELECT gm.showguestmapid
            FROM ww_showguestmap gm
            JOIN ww_shows s ON s.showid = gm.showid
            WHERE YEAR(s.showdate) = %s
            AND s.bestof = 0
            AND s.repeatshowid IS NULL
            UNION
            SELECT gm.showguestmapid
            FROM ww_showguestmap gm
            JOIN ww_shows s ON s.showid = gm.showid
            WHERE YEAR(s.showdate) = %s
            AND s.bestof = 1
            AND s.repeatshowid IS NULL
            AND gm.guestid NOT IN (
                SELECT gm.guestid
                FROM ww_showguestmap gm
                JOIN ww_shows s ON s.showid = gm.showid
                WHERE s.bestof = 0
                AND s.repeatshowid IS NULL
            )
        )
        AND g.guestslug <> 'none'
        AND (gm.guestscore >= 2 OR gm.exception = 1)
        AND (s.showdate <> '1998-05-02')
        ORDER BY s.showdate ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(
        query,
        (
            year,
            year,
        ),
    )
    results = cursor.fetchall()
    cursor.close()

    if not results:
        return None

    _appearances = []
    for row in results:
        _appearances.append(
            {
                "date": row["showdate"].isoformat(),
                "best_of": bool(row["bestof"]),
                "repeat_show": bool(row["repeatshowid"]),
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

    return _appearances
