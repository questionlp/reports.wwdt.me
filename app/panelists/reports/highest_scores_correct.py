# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Panelist Highest Average Score and Correct Answers Report Functions."""

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection


def retrieve_highest_average_scores_by_year(
    year: int,
    database_connection: MySQLConnection | PooledMySQLConnection,
    exclude_single_appearances: bool = False,
) -> dict[str, str | int] | None:
    """Retrieve panelists with the highest average score for a given year.

    Does not include Best Of and/or repeat shows.
    """
    if not database_connection.is_connected():
        database_connection.reconnect()

    if exclude_single_appearances:
        query = """
            SELECT p.panelist, p.panelistslug,
            COUNT(pm.showid) AS appearances,
            AVG(pm.panelistscore_decimal) AS average_score
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            WHERE YEAR(s.showdate) = %s
            AND s.showdate <> '2018-10-27'
            AND s.bestof = 0 AND s.repeatshowid IS NULL
            AND pm.panelistscore_decimal IS NOT NULL
            GROUP BY p.panelist, p.panelistslug
            HAVING COUNT(pm.showid) > 1
            ORDER BY AVG(pm.panelistscore_decimal) DESC,
            COUNT(pm.showid) DESC, p.panelist ASC;
        """
    else:
        query = """
            SELECT p.panelist, p.panelistslug,
            COUNT(pm.showid) AS appearances,
            AVG(pm.panelistscore_decimal) AS average_score
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            WHERE YEAR(s.showdate) = %s
            AND s.showdate <> '2018-10-27'
            AND s.bestof = 0 AND s.repeatshowid IS NULL
            AND pm.panelistscore_decimal IS NOT NULL
            GROUP BY p.panelist, p.panelistslug
            ORDER BY AVG(pm.panelistscore_decimal) DESC,
            COUNT(pm.showid) DESC, p.panelist ASC;
        """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (year,))
    results = cursor.fetchall()

    if not results:
        return None

    _panelists = {}
    for row in results:
        _panelists[row["panelistslug"]] = {
            "name": row["panelist"],
            "slug": row["panelistslug"],
            "appearances": row["appearances"],
            "average_score": row["average_score"],
        }

    return _panelists


def retrieve_highest_average_correct_answers_by_year(
    year: int,
    database_connection: MySQLConnection | PooledMySQLConnection,
    exclude_single_appearances: bool = False,
) -> dict[str, str | int] | None:
    """Retrieve panelists with the highest number of correct answers for a given year.

    Does not include Best Of and/or repeat shows.
    """
    if not database_connection.is_connected():
        database_connection.reconnect()

    if exclude_single_appearances:
        query = """
            SELECT p.panelist, p.panelistslug,
            COUNT(pm.showid) AS appearances,
            AVG(pm.panelistlrndcorrect_decimal) AS average_correct
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            WHERE YEAR(s.showdate) = %s
            AND s.showdate <> '2018-10-27'
            AND s.bestof = 0 AND s.repeatshowid IS NULL
            AND pm.panelistlrndcorrect_decimal IS NOT NULL
            GROUP BY p.panelist, p.panelistslug
            HAVING COUNT(pm.showid) > 1
            ORDER BY AVG(pm.panelistlrndcorrect_decimal) DESC,
            COUNT(pm.showid) DESC, p.panelist ASC;
        """
    else:
        query = """
            SELECT p.panelist, p.panelistslug,
            COUNT(pm.showid) AS appearances,
            AVG(pm.panelistlrndcorrect_decimal) AS average_correct
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            WHERE YEAR(s.showdate) = %s
            AND s.showdate <> '2018-10-27'
            AND s.bestof = 0 AND s.repeatshowid IS NULL
            AND pm.panelistlrndcorrect_decimal IS NOT NULL
            GROUP BY p.panelist, p.panelistslug
            ORDER BY AVG(pm.panelistlrndcorrect_decimal) DESC,
            COUNT(pm.showid) DESC, p.panelist ASC;
        """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (year,))
    results = cursor.fetchall()

    if not results:
        return None

    _panelists = {}
    for row in results:
        _panelists[row["panelistslug"]] = {
            "name": row["panelist"],
            "slug": row["panelistslug"],
            "appearances": row["appearances"],
            "average_correct": row["average_correct"],
        }

    return _panelists
