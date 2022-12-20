# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Panelist Appearances by Year Report Functions"""
from typing import Any, Dict, List, Union

import mysql.connector


def retrieve_panelist_appearance_counts(
    panelist_id: int, database_connection: mysql.connector.connect
) -> List[Dict[Union[str, int], int]]:
    """Retrieve yearly apperance count for the requested panelist ID"""

    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT YEAR(s.showdate) AS year, COUNT(p.panelist) AS count "
        "FROM ww_showpnlmap pm "
        "JOIN ww_shows s ON s.showid = pm.showid "
        "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
        "WHERE pm.panelistid = %s AND s.bestof = 0 "
        "AND s.repeatshowid IS NULL "
        "GROUP BY p.panelist, YEAR(s.showdate) "
        "ORDER BY p.panelist ASC, YEAR(s.showdate) ASC"
    )
    cursor.execute(query, (panelist_id,))
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    _appearances = {}
    total_appearances = 0
    for row in result:
        _appearances[row.year] = row.count
        total_appearances += row.count

    _appearances["total"] = total_appearances
    return _appearances


def retrieve_all_appearance_counts(
    database_connection: mysql.connector.connect,
) -> List[Dict[str, Any]]:
    """Retrieve all appearance counts for all panelists from the
    database"""

    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT DISTINCT p.panelistid, p.panelist, p.panelistslug "
        "FROM ww_showpnlmap pm "
        "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
        "JOIN ww_shows s ON s.showid = pm.showid "
        "WHERE s.bestof = 0 AND s.repeatshowid IS NULL "
        "ORDER BY p.panelist ASC"
    )
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    _panelists = []
    for row in result:
        panelist_id = row.panelistid
        _panelists.append(
            {
                "name": row.panelist,
                "slug": row.panelistslug,
                "appearances": retrieve_panelist_appearance_counts(
                    panelist_id=panelist_id, database_connection=database_connection
                ),
            }
        )

    return _panelists


def retrieve_all_years(database_connection: mysql.connector.connect) -> List[int]:
    """Retrieve a list of all available show years"""

    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT DISTINCT YEAR(s.showdate) AS year FROM ww_shows s "
        "ORDER BY YEAR(s.showdate) ASC"
    )
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    return [row.year for row in result]
