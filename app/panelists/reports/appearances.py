# -*- coding: utf-8 -*-
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Panelist Appearances Report Functions"""

from collections import OrderedDict
from typing import Dict, List
import mysql.connector

#region Retrieval Functions
def retrieve_all_panelists(database_connection: mysql.connector.connect
                          ) -> List[Dict]:
    """Retrieves a dictionary for all available panelists from the
    database"""

    cursor = database_connection.cursor(dictionary=True)
    query = ("SELECT p.panelistid, p.panelist, p.panelistslug "
             "FROM ww_panelists p "
             "WHERE p.panelist <> '<Multiple>' "
             "ORDER BY p.panelistslug ASC;")
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    panelists = []
    for row in result:
        panelist = OrderedDict()
        panelist["name"] = row["panelist"]
        panelist["slug"] = row["panelistslug"]
        panelists.append(panelist)

    return panelists

#endregion

#region Report Functions
def retrieve_first_most_recent_appearances(database_connection: mysql.connector.connect
                                          ) -> List[Dict]:
    """Retrieve first and most recent appearances for both regular
    and all shows for all panelists"""
    panelists = retrieve_all_panelists(database_connection)

    if not panelists:
        return None

    panelist_appearances = OrderedDict()
    for panelist in panelists:
        info = OrderedDict()
        info["name"] = panelist["name"]
        info["slug"] = panelist["slug"]
        info["first"] = None
        info["most_recent"] = None
        info["count"] = 0
        info["first_all"] = None
        info["most_recent_all"] = None
        info["count_all"] = 0
        panelist_appearances[panelist["slug"]] = info

    cursor = database_connection.cursor(dictionary=True)
    query = ("SELECT p.panelist, p.panelistslug, "
             "MIN(s.showdate) AS min, MAX(s.showdate) AS max "
             "FROM ww_showpnlmap pm "
             "JOIN ww_shows s ON s.showid = pm.showid "
             "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
             "WHERE s.bestof = 0 "
             "AND s.repeatshowid IS null "
             "AND p.panelist <> '<Multiple>' "
             "GROUP BY p.panelistid "
             "ORDER BY p.panelist ASC")
    cursor.execute(query)
    result = cursor.fetchall()

    if not result:
        return None

    for row in result:
        slug = row["panelistslug"]
        panelist_appearances[slug]["first"] = row["min"].isoformat()
        panelist_appearances[slug]["most_recent"] = row["max"].isoformat()

    query = ("SELECT p.panelist, p.panelistslug, COUNT(pm.panelistid) AS count "
             "FROM ww_showpnlmap pm "
             "JOIN ww_shows s ON s.showid = pm.showid "
             "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
             "WHERE s.bestof = 0 AND s.repeatshowid IS NULL "
             "AND p.panelist <> '<Multiple>' "
             "GROUP BY p.panelistid "
             "ORDER BY p.panelist ASC")
    cursor.execute(query)
    result = cursor.fetchall()

    if not result:
        return None

    for row in result:
        slug = row["panelistslug"]
        panelist_appearances[slug]["count"] = row["count"]

    query = ("SELECT p.panelist, p.panelistslug, COUNT(pm.panelistid) AS count "
             "FROM ww_showpnlmap pm "
             "JOIN ww_shows s ON s.showid = pm.showid "
             "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
             "WHERE p.panelist <> '<Multiple>' "
             "GROUP BY p.panelistid "
             "ORDER BY p.panelist ASC")
    cursor.execute(query)
    result = cursor.fetchall()

    if not result:
        return None

    for row in result:
        slug = row["panelistslug"]
        panelist_appearances[slug]["count_all"] = row["count"]

    query = ("SELECT p.panelist, p.panelistslug, "
             "MIN(s.showdate) AS min, MAX(s.showdate) AS max "
             "FROM ww_showpnlmap pm "
             "JOIN ww_shows s ON s.showid = pm.showid "
             "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
             "WHERE p.panelist <> '<Multiple>' "
             "GROUP BY p.panelistid "
             "ORDER BY p.panelist ASC")
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return panelist_appearances

    for row in result:
        slug = row["panelistslug"]
        panelist_appearances[slug]["first_all"] = row["min"].isoformat()
        panelist_appearances[slug]["most_recent_all"] = row["max"].isoformat()

    return panelist_appearances

#endregion
