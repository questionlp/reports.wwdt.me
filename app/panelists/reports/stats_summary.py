# -*- coding: utf-8 -*-
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Panelist Statistics Summary Report Functions"""

from collections import OrderedDict
from typing import Dict, List, Text
import mysql.connector
import numpy

def retrieve_all_panelists(database_connection: mysql.connector.connect
                          ) -> Dict:
    """Retrieves a dictionary for all available panelists from the
    database"""

    cursor = database_connection.cursor(dictionary=True)
    query = ("SELECT p.panelist, p.panelistslug FROM ww_panelists p "
             "WHERE p.panelist <> '<Multiple>' "
             "ORDER BY p.panelistslug ASC;")
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    panelists = OrderedDict()
    for row in result:
        slug = row["panelistslug"]
        name = row["panelist"]
        panelists[slug] = name

    return panelists

def retrieve_appearances_by_panelist(panelist_slug: Text,
                                     database_connection: mysql.connector.connect
                                     ) -> Dict:
    """Retrieve appearance data for the requested panelist by the
    panelist's slug string"""

    cursor = database_connection.cursor(dictionary=True)
    query = ("SELECT ( "
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
             "AS withscores;")
    cursor.execute(query, (panelist_slug, panelist_slug, panelist_slug, ))
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return None

    appearances = OrderedDict()
    appearances["regular"] = result["regular"]
    appearances["all"] = result["allshows"]
    appearances["with_scores"] = result["withscores"]

    return appearances

def retrieve_scores_by_panelist(panelist_slug: Text,
                                database_connection: mysql.connector.connect
                               ) -> List[int]:
    """Retrieve all scores for the requested panelist by the panelist's
    slug string"""

    cursor = database_connection.cursor(dictionary=True)
    query = ("SELECT pm.panelistscore FROM ww_showpnlmap pm "
             "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
             "JOIN ww_shows s ON s.showid = pm.showid "
             "WHERE s.bestof = 0 AND s.repeatshowid IS NULL "
             "AND p.panelistslug = %s "
             "AND pm.panelistscore IS NOT NULL;")
    cursor.execute(query, (panelist_slug, ))
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    scores = []
    for row in result:
        scores.append(row["panelistscore"])

    return scores

def retrieve_all_panelists_stats(database_connection: mysql.connector.connect
                                ) -> Dict:
    """Retrieve appearance and score statistics for all available
    panelists and calculates common statistics for each panelist"""

    panelists = retrieve_all_panelists(database_connection)

    if not panelists:
        return None

    all_stats = OrderedDict()
    for panelist_slug, _ in panelists.items():
        all_stats[panelist_slug] = OrderedDict()
        stats = OrderedDict()

        appearance_data = retrieve_appearances_by_panelist(panelist_slug,
                                                           database_connection)
        all_stats[panelist_slug]["appearances"] = appearance_data

        scores = retrieve_scores_by_panelist(panelist_slug,
                                             database_connection)

        if scores:
            stats["minimum"] = int(numpy.amin(scores))
            stats["maximum"] = int(numpy.amax(scores))
            stats["mean"] = round(numpy.mean(scores), 4)
            stats["median"] = int(numpy.median(scores))
            stats["standard_deviation"] = round(numpy.std(scores), 4)
            stats["total"] = int(numpy.sum(scores))
            all_stats[panelist_slug]["stats"] = stats
        else:
            all_stats[panelist_slug]["stats"] = None

    return all_stats
