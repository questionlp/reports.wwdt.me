# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Panelist Appearances Report Functions"""
from typing import Any, Dict, List

import mysql.connector


def retrieve_all_panelists(
    database_connection: mysql.connector.connect,
) -> List[Dict[str, str]]:
    """Retrieves a dictionary for all available panelists from the
    database"""

    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT p.panelistid, p.panelist, p.panelistslug "
        "FROM ww_panelists p "
        "WHERE p.panelist <> '<Multiple>' "
        "ORDER BY p.panelistslug ASC;"
    )
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    panelists = []
    for row in result:
        panelists.append(
            {
                "name": row.panelist,
                "slug": row.panelistslug,
            }
        )

    return panelists


def retrieve_first_most_recent_appearances(
    database_connection: mysql.connector.connect,
) -> List[Dict[str, Any]]:
    """Retrieve first and most recent appearances for both regular
    and all shows for all panelists"""
    panelists = retrieve_all_panelists(database_connection=database_connection)

    if not panelists:
        return None

    panelist_appearances = {}
    for panelist in panelists:
        panelist_appearances[panelist["slug"]] = {
            "name": panelist["name"],
            "slug": panelist["slug"],
            "first": None,
            "most_recent": None,
            "count": 0,
            "first_all": None,
            "most_recent_all": None,
            "count_all": 0,
        }

    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT p.panelist, p.panelistslug, "
        "MIN(s.showdate) AS min, MAX(s.showdate) AS max "
        "FROM ww_showpnlmap pm "
        "JOIN ww_shows s ON s.showid = pm.showid "
        "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
        "WHERE s.bestof = 0 "
        "AND s.repeatshowid IS null "
        "AND p.panelist <> '<Multiple>' "
        "GROUP BY p.panelistid "
        "ORDER BY p.panelist ASC"
    )
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    for row in result:
        slug = row.panelistslug
        panelist_appearances[slug]["first"] = row.min.isoformat()
        panelist_appearances[slug]["most_recent"] = row.max.isoformat()

    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT p.panelist, p.panelistslug, COUNT(pm.panelistid) AS count "
        "FROM ww_showpnlmap pm "
        "JOIN ww_shows s ON s.showid = pm.showid "
        "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
        "WHERE s.bestof = 0 AND s.repeatshowid IS NULL "
        "AND p.panelist <> '<Multiple>' "
        "GROUP BY p.panelistid "
        "ORDER BY p.panelist ASC"
    )
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    for row in result:
        slug = row.panelistslug
        panelist_appearances[slug]["count"] = row.count

    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT p.panelist, p.panelistslug, COUNT(pm.panelistid) AS count "
        "FROM ww_showpnlmap pm "
        "JOIN ww_shows s ON s.showid = pm.showid "
        "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
        "WHERE p.panelist <> '<Multiple>' "
        "GROUP BY p.panelistid "
        "ORDER BY p.panelist ASC"
    )
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    for row in result:
        slug = row.panelistslug
        panelist_appearances[slug]["count_all"] = row.count

    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT p.panelist, p.panelistslug, "
        "MIN(s.showdate) AS min, MAX(s.showdate) AS max "
        "FROM ww_showpnlmap pm "
        "JOIN ww_shows s ON s.showid = pm.showid "
        "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
        "WHERE p.panelist <> '<Multiple>' "
        "GROUP BY p.panelistid "
        "ORDER BY p.panelist ASC"
    )
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return panelist_appearances

    for row in result:
        slug = row.panelistslug
        panelist_appearances[slug]["first_all"] = row.min.isoformat()
        panelist_appearances[slug]["most_recent_all"] = row.max.isoformat()

    return panelist_appearances
