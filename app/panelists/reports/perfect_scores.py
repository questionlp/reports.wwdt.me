# Copyright (c) 2018-2023 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Panelist Perfect Scores Report Functions."""
import mysql.connector
from flask import current_app


def retrieve_perfect_score_counts(
    database_connection: mysql.connector.connect, use_decimal_scores: bool = False
) -> dict[str, str | int]:
    """Returns a dictionary with counts of how many times panelists have scored a "perfect" score.

    A "perfect" score is one that greater than or equals to 20 points. Excludes
    Best Of and repeat shows.
    """
    if (
        use_decimal_scores
        and not current_app.config["app_settings"]["has_decimal_scores_column"]
    ):
        return None

    if not database_connection.is_connected():
        database_connection.reconnect()

    if use_decimal_scores:
        query = """
            SELECT p.panelist, ANY_VALUE(p.panelistslug) AS panelistslug,
            COUNT(p.panelist) AS count
            FROM ww_showpnlmap pm
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE pm.panelistscore_decimal >= 20
            AND s.bestof = 0 AND s.repeatshowid IS NULL
            GROUP BY p.panelist
            ORDER BY COUNT(p.panelist) DESC;
            """
    else:
        query = """
            SELECT p.panelist, ANY_VALUE(p.panelistslug) AS panelistslug,
            COUNT(p.panelist) AS count
            FROM ww_showpnlmap pm
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE pm.panelistscore >= 20
            AND s.bestof = 0 AND s.repeatshowid IS NULL
            GROUP BY p.panelist
            ORDER BY COUNT(p.panelist) DESC;
            """
    cursor = database_connection.cursor(named_tuple=True)
    cursor.execute(query)
    results = cursor.fetchall()

    if not results:
        return None

    panelists = {}
    for row in results:
        panelists[row.panelistslug] = {
            "name": row.panelist,
            "slug": row.panelistslug,
            "more_perfect": row.count,
        }

    if use_decimal_scores:
        query = """
            SELECT p.panelist, ANY_VALUE(p.panelistslug) AS panelistslug,
            COUNT(p.panelist) AS count
            FROM ww_showpnlmap pm
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE pm.panelistscore_decimal = 20
            AND s.bestof = 0 AND s.repeatshowid IS NULL
            GROUP BY p.panelist;
            """
    else:
        query = """
            SELECT p.panelist, ANY_VALUE(p.panelistslug) AS panelistslug,
            COUNT(p.panelist) AS count
            FROM ww_showpnlmap pm
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE pm.panelistscore = 20
            AND s.bestof = 0 AND s.repeatshowid IS NULL
            GROUP BY p.panelist;
            """
    cursor.execute(query)
    results = cursor.fetchall()

    if not results:
        return None

    for row in results:
        panelists[row.panelistslug]["perfect"] = row.count

    return panelists
