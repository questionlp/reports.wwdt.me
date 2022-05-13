# -*- coding: utf-8 -*-
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Panelist Debut by Year Report Functions"""

from collections import OrderedDict
from typing import Dict, List
import mysql.connector

from reports.panelist import stats_summary

#region Retrieval Functions
def retrieve_show_years(database_connection: mysql.connector.connect
                       ) -> List[int]:
    """Retrieve a list of all show years"""

    cursor = database_connection.cursor(dictionary=True)
    query = ("SELECT DISTINCT YEAR(showdate) AS year "
             "FROM ww_shows "
             "ORDER BY showdate ASC;")
    cursor.execute(query, )
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    years = []
    for row in result:
        years.append(row["year"])

    return years

def retrieve_show_info(show_date: str,
                       database_connection: mysql.connector.connect
                      ) -> Dict:
    """Retrieve show host, scorekeeper and Not My Job guest for the
    requested show ID"""

    cursor = database_connection.cursor(dictionary=True)
    query = ("SELECT s.showid, s.bestof, h.host, sk.scorekeeper "
             "FROM ww_showhostmap hm "
             "JOIN ww_hosts h ON h.hostid = hm.hostid "
             "JOIN ww_shows s ON s.showid = hm.showid "
             "JOIN ww_showskmap skm ON skm.showid = hm.showid "
             "JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid "
             "WHERE s.showdate = %s;")
    cursor.execute(query, (show_date, ))
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return None

    show_info = OrderedDict()
    show_info["id"] = result["showid"]
    show_info["best_of"] = bool(result["bestof"])
    show_info["host"] = result["host"]
    show_info["scorekeeper"] = result["scorekeeper"]

    return show_info

def retrieve_show_guests(show_id: int,
                         database_connection: mysql.connector.connect
                        ) -> List[str]:
    """Retrieves a list of Not My Job guest(s) for the requested
    show ID"""

    cursor = database_connection.cursor(dictionary=True)
    query = ("SELECT g.guest "
             "FROM ww_showguestmap gm "
             "JOIN ww_guests g ON g.guestid = gm.guestid "
             "WHERE gm.showid = %s "
             "AND g.guestid <> 76 "
             "ORDER BY gm.showguestmapid ASC;")
    cursor.execute(query, (show_id, ))
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    guests = []
    for row in result:
        guests.append(row["guest"])

    return guests

def retrieve_panelists_first_shows(database_connection: mysql.connector.connect
                                  ) -> Dict:
    """Returns an OrderedDict containing all panelists and their
    respective first shows"""

    cursor = database_connection.cursor(dictionary=True)
    query = ("SELECT p.panelistid, p.panelist, p.panelistslug, "
             "MIN(s.showdate) AS first, YEAR(MIN(s.showdate)) AS year "
             "FROM ww_showpnlmap pm "
             "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
             "JOIN ww_shows s ON s.showid = pm.showid "
             "WHERE p.panelist <> '<Multiple>' "
             "GROUP BY p.panelist "
             "ORDER BY MIN(s.showdate) ASC;")
    cursor.execute(query, )
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    panelists = OrderedDict()
    for row in result:
        info = OrderedDict()
        show_date = row["first"]
        show_info = retrieve_show_info(show_date,
                                       database_connection)
        show_id = show_info["id"]

        info["id"] = row["panelistid"]
        info["panelist_name"] = row["panelist"]
        info["panelist_slug"] = row["panelistslug"]
        info["show"] = row["first"].isoformat()
        info["show_id"] = show_id
        info["year"] = row["year"]
        info["best_of"] = show_info["best_of"]
        appearance_info = stats_summary.retrieve_appearances_by_panelist(info["panelist_slug"],
                                                                         database_connection)
        info["regular_appearances"] = appearance_info["regular"]
        info["host"] = show_info["host"]
        info["scorekeeper"] = show_info["scorekeeper"]

        info["guests"] = retrieve_show_guests(show_id,
                                              database_connection)

        panelists[info["panelist_slug"]] = info

    return panelists

#endregion

#region Report Functions
def panelist_debuts_by_year(database_connection: mysql.connector.connect
                           ) -> Dict:
    """Returns an OrderedDict of show years with a list of panelists'
    debut information"""

    show_years = retrieve_show_years(database_connection)
    panelists = retrieve_panelists_first_shows(database_connection)

    years_debut = OrderedDict()
    for year in show_years:
        years_debut[year] = []

    for panelist in panelists:
        panelist_info = panelists[panelist]
        years_debut[panelist_info["year"]].append(panelist_info)

    return years_debut

#endregion
