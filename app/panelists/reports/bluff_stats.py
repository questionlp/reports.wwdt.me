# Copyright (c) 2018-2023 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Panelist Bluff the Listener Statistics Report Functions."""
from typing import Any

import mysql.connector

from . import common


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
        JOIN ww_showdescriptions sd ON sd.showid = pm.showid
        JOIN ww_showbluffmap blm ON blm.showid = pm.showid
        WHERE pm.panelistid = %s
        AND sd.showdescription LIKE '%bluff%'
        AND s.repeatshowid IS NULL AND s.bestof = 0
        AND (blm.chosenbluffpnlid IS NOT NULL
        AND blm.correctbluffpnlid IS NOT NULL)
        ORDER BY s.showdate ASC;
        """
    cursor = database_connection.cursor(named_tuple=True)
    cursor.execute(query, (panelist_id,))
    result = cursor.fetchone()
    cursor.close()

    if not result:
        counts["appearances"] = None
    else:
        counts["appearances"] = result.appearances

    query = """
        SELECT COUNT(s.showdate) as appearances
        FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        JOIN ww_showdescriptions sd ON sd.showid = pm.showid
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

    if not result:
        counts["unique_best_of"] = None
    else:
        counts["unique_best_of"] = result.appearances

    return counts


def retrieve_all_panelist_bluff_stats(
    database_connection: mysql.connector.connect,
) -> list[dict[str, Any]]:
    """Retrieves a list of Bluff the Listener statistics for all panelists."""
    _panelists = common.retrieve_panelists(database_connection=database_connection)

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
