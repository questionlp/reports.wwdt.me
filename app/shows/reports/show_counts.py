# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Show Counts Report Functions."""

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection


def retrieve_show_counts_by_year(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> dict[int, int]:
    """Retrieve number of Regular, Best Of, Repeat and Repeat/Best Of shows broken down by year."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT DISTINCT YEAR(showdate) AS 'year' FROM ww_shows
        ORDER BY YEAR(showdate) ASC;
        """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    years = []
    for row in result:
        years.append(int(row["year"]))

    show_counts = {}
    for year in years:
        query = """
            SELECT
            (SELECT COUNT(showid) FROM ww_shows
                WHERE YEAR(showdate) = %s AND showdate <= NOW()
                AND bestof = 0 AND repeatshowid IS NULL) AS 'regular',
            (SELECT COUNT(showid) FROM ww_shows
                WHERE YEAR(showdate) = %s AND showdate <= NOW()
                AND bestof = 1 AND repeatshowid IS NULL) AS 'bestof',
            (SELECT COUNT(showid) FROM ww_shows
                WHERE YEAR(showdate) = %s AND showdate <= NOW()
                AND bestof = 0 AND repeatshowid IS NOT NULL) AS 'repeat',
            (SELECT COUNT(showid) FROM ww_shows
                WHERE YEAR(showdate) = %s AND showdate <= NOW()
                AND bestof = 1 AND repeatshowid IS NOT NULL) AS 'repeat_bestof';
            """
        cursor = database_connection.cursor(dictionary=True)
        cursor.execute(
            query,
            (
                year,
                year,
                year,
                year,
            ),
        )
        result = cursor.fetchone()
        cursor.close()

        if not result:
            show_counts[year] = None
        else:
            show_counts[year] = {
                "regular": result["regular"],
                "best_of": result["bestof"],
                "repeat": result["repeat"],
                "repeat_best_of": result["repeat_bestof"],
                "total": (
                    result["regular"]
                    + result["bestof"]
                    + result["repeat"]
                    + result["repeat_bestof"]
                ),
            }

    return show_counts
