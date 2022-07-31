# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Panelist Statistics Summary Report Functions"""
from typing import Any, Dict, List

import mysql.connector
import numpy

from . import common


def retrieve_appearances_by_panelist(
    panelist_slug: str, database_connection: mysql.connector.connect
) -> Dict[str, int]:
    """Retrieve appearance data for the requested panelist by the
    panelist's slug string"""

    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT ( "
        "SELECT COUNT(pm.showid) FROM ww_showpnlmap pm "
        "JOIN ww_shows s ON s.showid = pm.showid "
        "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
        "WHERE s.bestof = 0 AND s.repeatshowid IS NULL AND "
        "p.panelistslug = %s ) AS regular, ( "
        "SELECT COUNT(pm.showid) FROM ww_showpnlmap pm "
        "JOIN ww_shows s ON s.showid = pm.showid "
        "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
        "WHERE p.panelistslug = %s ) AS allshows, ( "
        "SELECT COUNT(pm.panelistid) FROM ww_showpnlmap pm "
        "JOIN ww_shows s ON pm.showid = s.showid "
        "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
        "WHERE p.panelistslug = %s AND s.bestof = 0 AND "
        "s.repeatshowid IS NULL "
        "AND pm.panelistscore IS NOT NULL ) "
        "AS withscores;"
    )
    cursor.execute(
        query,
        (
            panelist_slug,
            panelist_slug,
            panelist_slug,
        ),
    )
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return None

    return {
        "regular": result.regular,
        "all": result.allshows,
        "with_scores": result.withscores,
    }


def retrieve_scores_by_panelist(
    panelist_slug: str, database_connection: mysql.connector.connect
) -> List[int]:
    """Retrieve all scores for the requested panelist by the panelist's
    slug string"""

    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT pm.panelistscore FROM ww_showpnlmap pm "
        "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
        "JOIN ww_shows s ON s.showid = pm.showid "
        "WHERE s.bestof = 0 AND s.repeatshowid IS NULL "
        "AND p.panelistslug = %s "
        "AND pm.panelistscore IS NOT NULL;"
    )
    cursor.execute(query, (panelist_slug,))
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    return [row.panelistscore for row in result]


def retrieve_all_panelists_stats(
    database_connection: mysql.connector.connect,
) -> Dict[str, Any]:
    """Retrieve appearance and score statistics for all available
    panelists and calculates common statistics for each panelist"""

    panelists = common.retrieve_panelists(database_connection=database_connection)

    if not panelists:
        return None

    all_stats = {}

    # for panelist_slug, _ in panelists.items():
    for panelist in panelists:
        panelist_slug = panelist["slug"]
        all_stats[panelist_slug] = {
            "appearances": retrieve_appearances_by_panelist(
                panelist_slug=panelist_slug, database_connection=database_connection
            ),
        }

        scores = retrieve_scores_by_panelist(
            panelist_slug=panelist_slug, database_connection=database_connection
        )
        if scores:
            all_stats[panelist_slug]["stats"] = {
                "minimum": int(numpy.amin(scores)),
                "maximum": int(numpy.amax(scores)),
                "mean": round(numpy.mean(scores), 4),
                "median": int(numpy.median(scores)),
                "standard_deviation": round(numpy.std(scores), 4),
                "total": int(numpy.sum(scores)),
            }
        else:
            all_stats[panelist_slug]["stats"] = None

    return all_stats
