# -*- coding: utf-8 -*-
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Panelist Apperances by Year Report Functions"""

from collections import OrderedDict
from typing import List, Dict
import mysql.connector

#region Retrieval Functions
def retrieve_panelist_appearance_counts(panelist_id: int,
                                        database_connection: mysql.connector.connect
                                       ) -> List[Dict]:
    """Retrieve yearly apperance count for the requested panelist ID"""

    cursor = database_connection.cursor()
    query = ("SELECT YEAR(s.showdate) AS year, COUNT(p.panelist) AS count "
             "FROM ww_showpnlmap pm "
             "JOIN ww_shows s ON s.showid = pm.showid "
             "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
             "WHERE pm.panelistid = %s AND s.bestof = 0 "
             "AND s.repeatshowid IS NULL "
             "GROUP BY p.panelist, YEAR(s.showdate) "
             "ORDER BY p.panelist ASC, YEAR(s.showdate) ASC")
    cursor.execute(query, (panelist_id, ))
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    appearances = OrderedDict()
    total_appearances = 0
    for row in result:
        appearances[row[0]] = row[1]
        total_appearances += row[1]

    appearances["total"] = total_appearances
    return appearances

def retrieve_all_appearance_counts(database_connection: mysql.connector.connect
                                  ) -> List[Dict]:
    """Retrieve all appearance counts for all panelists from the
    database"""

    cursor = database_connection.cursor(dictionary=True)
    query = ("SELECT DISTINCT p.panelistid, p.panelist, p.panelistslug "
             "FROM ww_showpnlmap pm "
             "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
             "JOIN ww_shows s ON s.showid = pm.showid "
             "WHERE s.bestof = 0 AND s.repeatshowid IS NULL "
             "ORDER BY p.panelist ASC")
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    panelists = []
    for row in result:
        panelist = {}
        panelist_id = row["panelistid"]
        panelist["name"] = row["panelist"]
        panelist["slug"] = row["panelistslug"]
        appearances = retrieve_panelist_appearance_counts(panelist_id=panelist_id,
                                                          database_connection=database_connection)
        panelist["appearances"] = appearances
        panelists.append(panelist)

    return panelists

def retrieve_all_years(database_connection: mysql.connector.connect) -> List[int]:
    """Retrieve a list of all available show years"""

    cursor = database_connection.cursor()
    query = ("SELECT DISTINCT YEAR(s.showdate) FROM ww_shows s "
             "ORDER BY YEAR(s.showdate) ASC")
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    years = []
    for row in result:
        years.append(row[0])

    return years

#endregion
