# -*- coding: utf-8 -*-
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Panelist vs Panelist Scoring Report Functions"""

from collections import OrderedDict
from typing import Dict, List
import mysql.connector

#region Retrieval Functions
def retrieve_common_shows(database_connection: mysql.connector.connect,
                          panelist_slug_1: str,
                          panelist_slug_2: str
                         ) -> List[int]:
    """Retrieve shows in which the two panelists have appeared
    together on a panel, excluding Best Of, Repeats and the 20th
    Anniversary special"""

    cursor = database_connection.cursor(dictionary=True)
    query = ("SELECT pm.showid FROM ww_showpnlmap pm "
             "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
             "JOIN ww_shows s ON s.showid = pm.showid "
             "WHERE p.panelistslug IN (%s, %s) "
             "AND s.showdate <> '2018-10-27' "
             "AND s.bestof = 0 AND s.repeatshowid IS NULL "
             "AND pm.panelistscore IS NOT NULL "
             "GROUP BY pm.showid "
             "HAVING COUNT(pm.showid) = 2 "
             "ORDER BY s.showdate ASC;")
    cursor.execute(query, (panelist_slug_1, panelist_slug_2, ))
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    shows = []
    for row in result:
        shows.append(row["showid"])

    return shows

def retrieve_panelists_scores(database_connection: mysql.connector.connect,
                              show_ids: List[int],
                              panelist_slug_a: str,
                              panelist_slug_b: str,
                             ) -> Dict:
    """Retrieves panelists scores for the two requested panelists"""

    if not show_ids:
        return None

    show_scores = OrderedDict()
    for show_id in show_ids:
        cursor = database_connection.cursor(dictionary=True)

        query = ("SELECT s.showdate, p.panelist, p.panelistslug, "
                 "pm.panelistscore, pm.showpnlrank FROM ww_showpnlmap pm "
                 "JOIN ww_shows s ON s.showid = pm.showid "
                 "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
                 "WHERE s.showid = %s "
                 "AND p.panelistslug IN (%s, %s);")
        cursor.execute(query, (show_id, panelist_slug_a, panelist_slug_b, ))
        result = cursor.fetchall()

        if not result:
            return None

        for row in result:
            show_date = row["showdate"].isoformat()
            if show_date not in show_scores:
                show_scores[show_date] = OrderedDict()

            panelist_info = OrderedDict()
            panelist_slug = row["panelistslug"]
            panelist_info["slug"] = panelist_slug
            panelist_info["name"] = row["panelist"]
            panelist_info["score"] = row["panelistscore"]
            panelist_info["rank"] = row["showpnlrank"]
            show_scores[show_date][panelist_slug] = panelist_info

    return show_scores

#endregion
