# -*- coding: utf-8 -*-
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Panelist Single Appearance Report Functions"""

from collections import OrderedDict
from typing import Dict, List
import mysql.connector

#region Retrieval Functions
def retrieve_single_appearances(database_connection: mysql.connector.connect
                               ) -> List[Dict]:
    """Retrieve a list of panelists that have only made a single
    appearance on the show"""

    panelists = []
    cursor = database_connection.cursor(dictionary=True)
    query = ("SELECT p.panelist, p.panelistslug, s.showdate, "
             "pm.panelistscore, pm.showpnlrank FROM ww_showpnlmap pm "
             "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
             "JOIN ww_shows s ON s.showid = pm.showid "
             "WHERE pm.showpnlmapid IN ( "
             "SELECT pm.showpnlmapid "
             "FROM ww_showpnlmap pm "
             "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
             "JOIN ww_shows s ON s.showid = pm.showid "
             "WHERE s.bestof = 0 AND s.repeatshowid IS NULL "
             "GROUP BY p.panelist "
             "HAVING COUNT(p.panelist) = 1 ) "
             "ORDER BY p.panelist ASC;")
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    for row in result:
        panelist = OrderedDict()
        panelist["name"] = row["panelist"]
        panelist["slug"] = row["panelistslug"]
        panelist["appearance"] = row["showdate"].isoformat()
        panelist["score"] = row["panelistscore"]
        panelist["rank"] = row["showpnlrank"]
        panelists.append(panelist)

    return panelists

#endregion
