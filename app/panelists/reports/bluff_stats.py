# Copyright (c) 2018-2023 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Panelist Bluff the Listener Statistics Report Functions."""
from typing import Any

import mysql.connector

from .common import retrieve_panelists


def empty_years_bluff(database_connection: mysql.connector.connect) -> dict[int, int]:
    """Retrieve a dictionary containing a list of available years as keys and zeroes for values."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    # Retrieve available show years
    cursor = database_connection.cursor(named_tuple=True)
    query = """
        SELECT DISTINCT YEAR(showdate) AS year
        FROM ww_shows
        ORDER BY YEAR(showdate) ASC;
        """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    return {
        row.year: {
            "chosen": 0,
            "correct": 0,
            "appearances": 0,
            "unique_best_of": 0,
        }
        for row in result
    }


def retrieve_panelist_bluff_counts(
    panelist_id: int, database_connection: mysql.connector.connect
) -> dict[str, Any]:
    """Retrieves a dictionary containing Bluff the Listener counts for a panelist.

    Returned is the number of times a panelist's Bluff story was chosen and the
    number of times a panelist had the correct story.
    """
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT (
        SELECT COUNT(blm.showid) FROM ww_showbluffmap blm
        JOIN ww_panelists p ON p.panelistid = blm.chosenbluffpnlid
        JOIN ww_shows s ON s.showid = blm.showid
        WHERE blm.chosenbluffpnlid = %s
        AND s.repeatshowid IS NULL
        AND (s.bestof = 0 OR (s.bestof = 1 AND s.bestofuniquebluff = 1))
        ) AS chosen, (
        SELECT COUNT(blm.showid) FROM ww_showbluffmap blm
        JOIN ww_panelists p ON p.panelistid = blm.correctbluffpnlid
        JOIN ww_shows s ON s.showid = blm.showid
        WHERE blm.correctbluffpnlid = %s
        AND s.repeatshowid IS NULL
        AND (s.bestof = 0 OR (s.bestof = 1 AND s.bestofuniquebluff = 1))
        ) AS correct;
        """
    cursor = database_connection.cursor(named_tuple=True)
    cursor.execute(
        query,
        (
            panelist_id,
            panelist_id,
        ),
    )
    result = cursor.fetchone()

    counts = {}
    if not result:
        counts["chosen"] = 0
        counts["correct"] = 0
    else:
        counts["chosen"] = result.chosen
        counts["correct"] = result.correct

    query = """
        SELECT COUNT(s.showdate) as appearances
        FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        JOIN ww_showbluffmap blm ON blm.showid = pm.showid
        WHERE pm.panelistid = %s
        AND s.repeatshowid IS NULL AND s.bestof = 0
        AND (blm.chosenbluffpnlid IS NOT NULL
        AND blm.correctbluffpnlid IS NOT NULL)
        ORDER BY s.showdate ASC;
        """
    cursor = database_connection.cursor(named_tuple=True)
    cursor.execute(query, (panelist_id,))
    result = cursor.fetchone()
    cursor.close()

    counts["appearances"] = result.appearances if result else None

    query = """
        SELECT COUNT(s.showdate) as appearances
        FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        JOIN ww_showbluffmap blm ON blm.showid = pm.showid
        WHERE pm.panelistid = %s
        AND s.repeatshowid IS NULL
        AND s.bestof = 1 AND s.bestofuniquebluff = 1
        AND (blm.chosenbluffpnlid IS NOT NULL
        AND blm.correctbluffpnlid IS NOT NULL)
        ORDER BY s.showdate ASC;
        """
    cursor = database_connection.cursor(named_tuple=True)
    cursor.execute(query, (panelist_id,))
    result = cursor.fetchone()
    cursor.close()

    counts["unique_best_of"] = result.appearances if result else None

    return counts


def retrieve_all_panelist_bluff_stats(
    database_connection: mysql.connector.connect,
) -> list[dict[str, Any]]:
    """Retrieves a list of Bluff the Listener statistics for all panelists."""
    _panelists = retrieve_panelists(database_connection=database_connection)

    if not _panelists:
        return None

    stats = []
    for panelist in _panelists:
        counts = retrieve_panelist_bluff_counts(
            panelist_id=panelist["id"], database_connection=database_connection
        )
        if counts and (counts["correct"] or counts["chosen"]):
            panelist.update(counts)
            stats.append(panelist)

    return stats


def retrieve_panelist_bluffs_by_year(
    panelist_slug: str,
    database_connection: mysql.connector.connect,
) -> dict[int, int]:
    """Retrieve a panelist's Bluff the Listener statistics per year."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
    SELECT YEAR(s.showdate) AS year, count(blm.chosenbluffpnlid) AS chosen
    FROM ww_showbluffmap blm
    JOIN ww_shows s ON s.showid = blm.showid
    JOIN ww_panelists p ON p.panelistid = blm.chosenbluffpnlid
    WHERE p.panelistslug = %s
    GROUP BY YEAR(s.showdate)
    ORDER BY YEAR(s.showdate) ASC;
    """
    cursor = database_connection.cursor(named_tuple=True)
    cursor.execute(query, (panelist_slug,))
    chosen_results = cursor.fetchall()

    query = """
    SELECT YEAR(s.showdate) AS year, count(blm.correctbluffpnlid) AS correct
    FROM ww_showbluffmap blm
    JOIN ww_shows s ON s.showid = blm.showid
    JOIN ww_panelists p ON p.panelistid = blm.correctbluffpnlid
    WHERE p.panelistslug = %s
    GROUP BY YEAR(s.showdate)
    ORDER BY YEAR(s.showdate) ASC;
    """
    cursor = database_connection.cursor(named_tuple=True)
    cursor.execute(query, (panelist_slug,))
    correct_results = cursor.fetchall()

    query = """
        SELECT YEAR(s.showdate) AS year, COUNT(s.showdate) AS appearances
        FROM ww_showpnlmap pm
        JOIN ww_showbluffmap blm ON blm.showid = pm.showid
        JOIN ww_shows s ON s.showid = pm.showid
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        WHERE p.panelistslug = %s
        AND s.repeatshowid IS NULL AND s.bestof = 0
        AND (blm.chosenbluffpnlid IS NOT NULL
        AND blm.correctbluffpnlid IS NOT NULL)
        GROUP BY YEAR(s.showdate)
        ORDER BY YEAR(s.showdate) ASC;
        """
    cursor = database_connection.cursor(named_tuple=True)
    cursor.execute(query, (panelist_slug,))
    appearance_results = cursor.fetchall()

    query = """
        SELECT YEAR(s.showdate) AS year, COUNT(s.showdate) AS appearances
        FROM ww_showpnlmap pm
        JOIN ww_showbluffmap blm ON blm.showid = pm.showid
        JOIN ww_shows s ON s.showid = pm.showid
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        WHERE p.panelistslug = %s
        AND s.repeatshowid IS NULL
        AND s.bestof = 1 AND s.bestofuniquebluff = 1
        AND (blm.chosenbluffpnlid IS NOT NULL
        AND blm.correctbluffpnlid IS NOT NULL)
        GROUP BY YEAR(s.showdate)
        ORDER BY YEAR(s.showdate) ASC;
        """
    cursor = database_connection.cursor(named_tuple=True)
    cursor.execute(query, (panelist_slug,))
    unique_bluff_appearance_results = cursor.fetchall()
    cursor.close()

    stats = empty_years_bluff(database_connection=database_connection)
    for row in chosen_results:
        stats[row.year]["chosen"] = row.chosen

    for row in correct_results:
        stats[row.year]["correct"] = row.correct

    if appearance_results:
        for row in appearance_results:
            stats[row.year]["appearances"] = row.appearances

    if unique_bluff_appearance_results:
        for row in unique_bluff_appearance_results:
            stats[row.year]["unique_bluff_appearances"] = row.appearances

    return stats
