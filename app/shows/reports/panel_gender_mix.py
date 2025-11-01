# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
# pylint: disable=C0301
"""WWDTM Show Panel Gender Mix Report Functions."""

from typing import Any

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection


def retrieve_show_years(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[int]:
    """Retrieve a list of show years available in the database."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT DISTINCT YEAR(s.showdate) AS year FROM ww_shows s
        ORDER BY YEAR(s.showdate) ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    return [row["year"] for row in result]


def retrieve_panel_gender_count_by_year(
    year: int, database_connection: MySQLConnection | PooledMySQLConnection
) -> int:
    """Return a count of shows for a year with counts of panel gender counts."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    counts = {}

    for gender_count in range(1, 4):
        query = """
            SELECT s.showdate FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            WHERE s.bestof = 0 AND s.repeatshowid IS NULL
            AND p.panelistgender = 'F'
            AND year(s.showdate) = %s
            AND s.showdate <> '2018-10-27' -- Exclude 25th anniversary special
            GROUP BY s.showdate
            HAVING COUNT(p.panelistgender) = %s;
        """
        cursor = database_connection.cursor(dictionary=False)
        cursor.execute(
            query,
            (
                year,
                gender_count,
            ),
        )
        cursor.fetchall()
        counts[f"{gender_count}F"] = cursor.rowcount
        cursor.close()

    # Get a count of all men panels due to potential excluded zero women
    # panel counts from above
    query = """
            SELECT s.showdate FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            WHERE s.bestof = 0 AND s.repeatshowid IS NULL
            AND p.panelistgender = 'M'
            AND year(s.showdate) = %s
            AND s.showdate <> '2018-10-27' -- Exclude 25th anniversary special
            GROUP BY s.showdate
            HAVING COUNT(p.panelistgender) = 3;
        """
    cursor = database_connection.cursor(dictionary=False)
    cursor.execute(query, (year,))
    cursor.fetchall()
    counts["0F"] = cursor.rowcount
    cursor.close()

    counts["total"] = sum(counts.values())
    return counts


def panel_gender_mix_breakdown(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> dict[str, Any]:
    """Return a dictionary of panel gender breakdown for all show years with count for each year."""
    show_years = retrieve_show_years(database_connection=database_connection)

    gender_mix_breakdown = {}
    for year in show_years:
        count = retrieve_panel_gender_count_by_year(
            year=year, database_connection=database_connection
        )
        gender_mix_breakdown[year] = count

    return gender_mix_breakdown
