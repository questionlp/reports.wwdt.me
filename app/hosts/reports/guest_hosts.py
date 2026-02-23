# Copyright (c) 2018-2026 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Guest Host Counts Report Functions."""

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from app.shows.reports.info import retrieve_show_years


def retrieve_guest_host_counts_by_year(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> dict[int, int | None] | None:
    """Retrieve a breakdown of guest host counts per year for all years.

    The returned dictionary uses year as the key.
    """
    if not database_connection.is_connected():
        database_connection.reconnect()

    _years = retrieve_show_years(database_connection=database_connection)
    if not _years:
        return None

    query = """
        SELECT YEAR(s.showdate) AS year, COUNT(s.showdate) AS count
        FROM ww_showhostmap hm
        JOIN ww_shows s ON s.showid = hm.showid
        WHERE hm.guest = 1
        GROUP BY YEAR(s.showdate)
        ORDER BY YEAR(s.showdate);
    """

    cursor = database_connection.cursor(dictionary=False)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    database_connection.close()

    if not results:
        return None

    _show_years = dict.fromkeys(_years, 0)
    for row in results:
        _show_years[row[0]] = row[1]

    return _show_years
