# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Panelist Bluff the Listener Statistics Report Functions"""
from typing import Any, Dict, List

import mysql.connector


def retrieve_all_panelists(
    database_connection: mysql.connector.connect,
) -> List[Dict[str, Any]]:
    """Retrieves a dictionary for all available panelists from the
    database"""

    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT p.panelistid, p.panelist, p.panelistslug "
        "FROM ww_panelists p "
        "WHERE p.panelist <> '<Multiple>' "
        "ORDER BY p.panelistslug ASC;"
    )
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    _panelists = []
    for row in result:
        _panelists.append(
            {
                "id": row.panelistid,
                "slug": row.panelistslug,
                "name": row.panelist,
            }
        )

    return _panelists


def retrieve_panelist_bluff_counts(
    panelist_id: int, database_connection: mysql.connector.connect
) -> Dict[str, Any]:
    """Retrieves a dictionary containing the count of the number of
    times a panelist's Bluff story was chosen and the number of times
    a panelist had the correct story"""

    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT ( "
        "SELECT COUNT(blm.showid) FROM ww_showbluffmap blm "
        "JOIN ww_panelists p ON p.panelistid = blm.chosenbluffpnlid "
        "JOIN ww_shows s ON s.showid = blm.showid "
        "WHERE blm.chosenbluffpnlid = %s "
        "AND s.repeatshowid IS NULL "
        "AND (s.bestof = 0 OR (s.bestof = 1 AND s.bestofuniquebluff = 1)) "
        ") AS chosen, ( "
        "SELECT COUNT(blm.showid) FROM ww_showbluffmap blm "
        "JOIN ww_panelists p ON p.panelistid = blm.correctbluffpnlid "
        "JOIN ww_shows s ON s.showid = blm.showid "
        "WHERE blm.correctbluffpnlid = %s "
        "AND s.repeatshowid IS NULL "
        "AND (s.bestof = 0 OR (s.bestof = 1 AND s.bestofuniquebluff = 1)) "
        ") AS correct;"
    )
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

    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT COUNT(s.showdate) as appearances "
        "FROM ww_showpnlmap pm "
        "JOIN ww_shows s ON s.showid = pm.showid "
        "JOIN ww_showdescriptions sd ON sd.showid = pm.showid "
        "JOIN ww_showbluffmap blm ON blm.showid = pm.showid "
        "WHERE pm.panelistid = %s "
        "AND sd.showdescription LIKE '%bluff%' "
        "AND s.repeatshowid IS NULL AND s.bestof = 0 "
        "AND (blm.chosenbluffpnlid IS NOT NULL "
        "AND blm.correctbluffpnlid IS NOT NULL) "
        "ORDER BY s.showdate ASC;"
    )
    cursor.execute(query, (panelist_id,))
    result = cursor.fetchone()
    cursor.close()

    if not result:
        counts["appearances"] = None
    else:
        counts["appearances"] = result.appearances

    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT COUNT(s.showdate) as appearances "
        "FROM ww_showpnlmap pm "
        "JOIN ww_shows s ON s.showid = pm.showid "
        "JOIN ww_showdescriptions sd ON sd.showid = pm.showid "
        "JOIN ww_showbluffmap blm ON blm.showid = pm.showid "
        "WHERE pm.panelistid = %s "
        "AND s.repeatshowid IS NULL "
        "AND s.bestof = 1 AND s.bestofuniquebluff = 1 "
        "AND (blm.chosenbluffpnlid IS NOT NULL "
        "AND blm.correctbluffpnlid IS NOT NULL) "
        "ORDER BY s.showdate ASC;"
    )
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
) -> List[Dict[str, Any]]:
    """Retrieves a list of Bluff the Listener statistics for all
    panelists"""

    if not database_connection.is_connected():
        database_connection.reconnect()

    _panelists = retrieve_all_panelists(database_connection=database_connection)

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
