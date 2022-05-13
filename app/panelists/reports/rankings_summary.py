# -*- coding: utf-8 -*-
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Panelist Rankings Summary Report Functions"""

from collections import OrderedDict
from typing import Dict
import mysql.connector

def retrieve_all_panelists(database_connection: mysql.connector.connect
                          ) -> Dict:
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

    panelists = OrderedDict()
    for row in result:
        panelist_id = row["panelistid"]
        slug = row["panelistslug"]
        name = row["panelist"]
        panelists[slug] = OrderedDict()
        panelists[slug]["name"] = name
        panelists[slug]["id"] = panelist_id

    return panelists

def retrieve_rankings_by_panelist(panelist_id: int,
                                  database_connection: mysql.connector.connect
                                 ) -> Dict:
    """Retrieves ranking statistics for the requested panelist"""

    cursor = database_connection.cursor(dictionary=True)
    query = ("SELECT ( "
             "SELECT COUNT(pm.showpnlrank) FROM ww_showpnlmap pm "
             "JOIN ww_shows s ON s.showid = pm.showid "
             "WHERE pm.panelistid = %s AND pm.showpnlrank = '1' AND "
             "s.bestof = 0 and s.repeatshowid IS NULL) as '1', ( "
             "SELECT COUNT(pm.showpnlrank) FROM ww_showpnlmap pm "
             "JOIN ww_shows s ON s.showid = pm.showid "
             "WHERE pm.panelistid = %s AND pm.showpnlrank = '1t' AND "
             "s.bestof = 0 and s.repeatshowid IS NULL) as '1t', ( "
             "SELECT COUNT(pm.showpnlrank) FROM ww_showpnlmap pm "
             "JOIN ww_shows s ON s.showid = pm.showid "
             "WHERE pm.panelistid = %s AND pm.showpnlrank = '2' AND "
             "s.bestof = 0 and s.repeatshowid IS NULL) as '2', ( "
             "SELECT COUNT(pm.showpnlrank) FROM ww_showpnlmap pm "
             "JOIN ww_shows s ON s.showid = pm.showid "
             "WHERE pm.panelistid = %s AND pm.showpnlrank = '2t' AND "
             "s.bestof = 0 and s.repeatshowid IS NULL) as '2t', ( "
             "SELECT COUNT(pm.showpnlrank) FROM ww_showpnlmap pm "
             "JOIN ww_shows s ON s.showid = pm.showid "
             "WHERE pm.panelistid = %s AND pm.showpnlrank = '3' AND "
             "s.bestof = 0 and s.repeatshowid IS NULL "
             ") as '3';")
    cursor.execute(query, (panelist_id,
                           panelist_id,
                           panelist_id,
                           panelist_id,
                           panelist_id, ))
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return None

    rankings = OrderedDict()
    rankings["first"] = result["1"]
    rankings["first_tied"] = result["1t"]
    rankings["second"] = result["2"]
    rankings["second_tied"] = result["2t"]
    rankings["third"] = result["3"]
    rankings["count"] = result["1"] + result["1t"] + \
                        result["2"] + result["2t"] + \
                        result["3"]

    if rankings["count"]:
        rankings["percent_first"] = round(100 * (rankings["first"] / rankings["count"]), 4)
        rankings["percent_first_tied"] = round(100 * (rankings["first_tied"] / rankings["count"]), 4)
        rankings["percent_second"] = round(100 * (rankings["second"] / rankings["count"]), 4)
        rankings["percent_second_tied"] = round(100 * (rankings["second_tied"] / rankings["count"]), 4)
        rankings["percent_third"] = round(100 * (rankings["third"] / rankings["count"]), 4)

    return rankings

def retrieve_all_panelist_rankings(database_connection: mysql.connector.connect
                                  ) -> Dict:
    """Returns ranking statistics for all available panelists"""

    panelists = retrieve_all_panelists(database_connection)
    if not panelists:
        return None

    panelist_rankings = OrderedDict()
    for panelist in panelists:
        panelist_id = panelists[panelist]["id"]
        rankings = retrieve_rankings_by_panelist(panelist_id,
                                                 database_connection)
        panelist_rankings[panelist] = rankings

    return panelist_rankings
