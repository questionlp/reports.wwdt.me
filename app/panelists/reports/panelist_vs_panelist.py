# -*- coding: utf-8 -*-
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Panelist vs Panelist Report Functions"""

from collections import OrderedDict
from typing import List, Dict
import mysql.connector

#region Retrieval Functions
def retrieve_panelists(database_connection: mysql.connector.connect
                      ) -> List[Dict]:
    """Retrieve panelists from the Stats Page database"""

    panelists = OrderedDict()
    try:
        cursor = database_connection.cursor()
        query = ("SELECT DISTINCT p.panelistid, p.panelist, p.panelistslug "
                 "FROM ww_showpnlmap pm "
                 "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
                 "WHERE pm.panelistscore IS NOT NULL "
                 "AND p.panelist <> '<Multiple>' "
                 "ORDER BY p.panelist ASC;")
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        for row in result:
            panelist_info = {}
            panelist_info["id"] = row[0]
            panelist_info["name"] = row[1]
            panelist_info["slug"] = row[2]
            panelists[panelist_info["slug"]] = panelist_info

        return panelists
    except mysql.connector.Error:
        return

def retrieve_panelist_appearances(panelists: Dict,
                                  database_connection: mysql.connector.connect
                                 ) -> Dict:
    """Retrieve panelist appearances from the Stats Page database"""

    panelist_appearances = OrderedDict()
    for _, panelist_info in panelists.items():
        try:
            appearances = []
            cursor = database_connection.cursor()
            query = ("SELECT s.showdate FROM ww_showpnlmap pm "
                     "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
                     "JOIN ww_shows s ON s.showid = pm.showid "
                     "WHERE p.panelistslug = %s "
                     "AND pm.panelistscore IS NOT NULL "
                     "AND s.bestof = 0 "
                     "AND s.repeatshowid IS NULL "
                     "ORDER BY s.showdate ASC;")
            cursor.execute(query, (panelist_info["slug"],))
            result = cursor.fetchall()
            cursor.close()

            if result:
                for appearance in result:
                    appearances.append(appearance[0].isoformat())

                panelist_appearances[panelist_info["slug"]] = appearances
        except mysql.connector.Error:
            return

    return panelist_appearances

def retrieve_show_scores(database_connection: mysql.connector.connect) -> Dict:
    """Retrieve scores for each show and panelist from the Stats Page
    Database"""

    shows = OrderedDict()

    try:
        cursor = database_connection.cursor()
        query = ("SELECT s.showdate, p.panelistslug, pm.panelistscore FROM ww_showpnlmap pm "
                 "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
                 "JOIN ww_shows s ON s.showid = pm.showid "
                 "WHERE s.bestof = 0 "
                 "AND s.repeatshowid IS NULL "
                 "AND pm.panelistscore IS NOT NULL "
                 "ORDER BY s.showdate ASC, pm.panelistscore DESC;")
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        if result:
            for show in result:
                show_date = show[0].isoformat()
                if show_date not in shows:
                    shows[show_date] = OrderedDict()

                panelist_slug = show[1]
                panelist_score = show[2]
                shows[show_date][panelist_slug] = panelist_score

        return shows
    except mysql.connector.Error:
        return

#endregion

#region Results Generation Functions
def generate_panelist_vs_panelist_results(panelists: Dict,
                                          panelist_appearances: Dict,
                                          show_scores: Dict
                                          ) -> Dict:
    """Generate panelist vs panelist results"""

    pvp_results = OrderedDict()
    for _, panelist_a in panelists.items():
        panelist_a = panelist_a["slug"]
        pvp_results[panelist_a] = OrderedDict()
        for _, panelist_b in panelists.items():
            panelist_b = panelist_b["slug"]
            if panelist_a != panelist_b:
                panelist_a_appearances = panelist_appearances[panelist_a]
                panelist_b_appearances = panelist_appearances[panelist_b]
                a_b_intersect = list(set(panelist_a_appearances) & set(panelist_b_appearances))
                a_b_intersect.sort()

                pvp_results[panelist_a][panelist_b] = OrderedDict()
                wins = 0
                draws = 0
                losses = 0
                for show in a_b_intersect:
                    panelist_a_score = show_scores[show][panelist_a]
                    panelist_b_score = show_scores[show][panelist_b]
                    if panelist_a_score > panelist_b_score:
                        wins = wins + 1
                    elif panelist_a_score == panelist_b_score:
                        draws = draws + 1
                    else:
                        losses = losses + 1

                pvp_results[panelist_a][panelist_b]["wins"] = wins
                pvp_results[panelist_a][panelist_b]["draws"] = draws
                pvp_results[panelist_a][panelist_b]["losses"] = losses
                pvp_results[panelist_a][panelist_b]["total"] = wins + draws + losses

    return pvp_results

#endregion
