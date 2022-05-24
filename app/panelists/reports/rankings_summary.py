# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Panelist Rankings Summary Report Functions"""
from typing import Any, Dict
import mysql.connector


def retrieve_all_panelists(
    database_connection: mysql.connector.connect,
) -> Dict[str, Any]:
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

    panelists = {}
    for row in result:
        panelists[row.panelistslug] = {
            "name": row.panelist,
            "id": row.panelistid,
        }

    return panelists


def retrieve_rankings_by_panelist(
    panelist_id: int, database_connection: mysql.connector.connect
) -> Dict[str, Any]:
    """Retrieves ranking statistics for the requested panelist"""

    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(dictionary=True)
    query = (
        "SELECT ( "
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
        ") as '3';"
    )
    cursor.execute(
        query,
        (
            panelist_id,
            panelist_id,
            panelist_id,
            panelist_id,
            panelist_id,
        ),
    )
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return None

    rankings = {
        "first": result["1"],
        "first_tied": result["1t"],
        "second": result["2"],
        "second_tied": result["2t"],
        "third": result["3"],
        "count": result["1"] + result["1t"] + result["2"] + result["2t"] + result["3"],
    }

    if rankings["count"]:
        rankings["percent_first"] = round(
            100 * (rankings["first"] / rankings["count"]), 4
        )
        rankings["percent_first_tied"] = round(
            100 * (rankings["first_tied"] / rankings["count"]), 4
        )
        rankings["percent_second"] = round(
            100 * (rankings["second"] / rankings["count"]), 4
        )
        rankings["percent_second_tied"] = round(
            100 * (rankings["second_tied"] / rankings["count"]), 4
        )
        rankings["percent_third"] = round(
            100 * (rankings["third"] / rankings["count"]), 4
        )

    return rankings


def retrieve_all_panelist_rankings(
    database_connection: mysql.connector.connect,
) -> Dict[str, Any]:
    """Returns ranking statistics for all available panelists"""

    if not database_connection.is_connected():
        database_connection.reconnect()

    panelists = retrieve_all_panelists(database_connection=database_connection)
    if not panelists:
        return None

    panelist_rankings = {}
    for panelist in panelists:
        panelist_id = panelists[panelist]["id"]
        rankings = retrieve_rankings_by_panelist(
            panelist_id=panelist_id, database_connection=database_connection
        )
        panelist_rankings[panelist] = rankings

    return panelist_rankings
