# -*- coding: utf-8 -*-
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Panelist Bluff the Listener Statistics Report Functions"""

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
        panelist["id"] = row["panelistid"]
        panelist["slug"] = row["panelistslug"]
        panelist["name"] = row["panelist"]
        panelists.append(panelist)

    return panelists

def retrieve_panelist_bluff_counts(panelist_id: int,
                                   database_connection: mysql.connector.connect
                                  ) -> Dict:
    """Retrieves a dictionary containing the count of the number of
    times a panelist's Bluff story was chosen and the number of times
    a panelist had the correct story"""

    counts = OrderedDict()
    cursor = database_connection.cursor(dictionary=True)
    query = ("SELECT ( "
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
             ") AS correct;")
    cursor.execute(query, (panelist_id, panelist_id, ))
    result = cursor.fetchone()

    if not result:
        counts["chosen"] = 0
        counts["correct"] = 0
    else:
        counts["chosen"] = result["chosen"]
        counts["correct"] = result["correct"]

    cursor = database_connection.cursor(dictionary=True)
    query = ("SELECT COUNT(s.showdate) as appearances "
             "FROM ww_showpnlmap pm "
             "JOIN ww_shows s ON s.showid = pm.showid "
             "JOIN ww_showdescriptions sd ON sd.showid = pm.showid "
             "JOIN ww_showbluffmap blm ON blm.showid = pm.showid "
             "WHERE pm.panelistid = %s "
             "AND sd.showdescription LIKE '%bluff%' "
             "AND s.repeatshowid IS NULL AND s.bestof = 0 "
             "AND (blm.chosenbluffpnlid IS NOT NULL "
             "AND blm.correctbluffpnlid IS NOT NULL) "
             "ORDER BY s.showdate ASC;")
    cursor.execute(query, (panelist_id, ))
    result = cursor.fetchone()
    cursor.close()

    if not result:
        counts["appearances"] = None
    else:
        counts["appearances"] = result["appearances"]

    cursor = database_connection.cursor(dictionary=True)
    query = ("SELECT COUNT(s.showdate) as appearances "
             "FROM ww_showpnlmap pm "
             "JOIN ww_shows s ON s.showid = pm.showid "
             "JOIN ww_showdescriptions sd ON sd.showid = pm.showid "
             "JOIN ww_showbluffmap blm ON blm.showid = pm.showid "
             "WHERE pm.panelistid = %s "
             "AND s.repeatshowid IS NULL "
             "AND s.bestof = 1 AND s.bestofuniquebluff = 1 "
             "AND (blm.chosenbluffpnlid IS NOT NULL "
             "AND blm.correctbluffpnlid IS NOT NULL) "
             "ORDER BY s.showdate ASC;")
    cursor.execute(query, (panelist_id, ))
    result = cursor.fetchone()
    cursor.close()

    if not result:
        counts["unique_best_of"] = None
    else:
        counts["unique_best_of"] = result["appearances"]

    return counts

def retrieve_all_panelist_bluff_stats(database_connection: mysql.connector.connect
                                     ) -> List[Dict]:
    """Retrieves a list of Bluff the Listener statistics for all
    panelists"""

    panelists = retrieve_all_panelists(database_connection)

    if not panelists:
        return None

    stats = []
    for panelist in panelists:
        counts = retrieve_panelist_bluff_counts(panelist["id"],
                                                database_connection)
        if counts  and (counts["correct"] or counts["chosen"]):
            panelist.update(counts)
            stats.append(panelist)

    return stats

#endregion
