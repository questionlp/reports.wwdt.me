# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Panelist Debut by Year Report Functions"""
from typing import Any, Dict, List

import mysql.connector

from .stats_summary import retrieve_appearances_by_panelist


def retrieve_show_years(database_connection: mysql.connector.connect) -> List[int]:
    """Retrieve a list of all show years"""

    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT DISTINCT YEAR(showdate) AS year "
        "FROM ww_shows "
        "ORDER BY showdate ASC;"
    )
    cursor.execute(
        query,
    )
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    return [row.year for row in result]


def retrieve_show_info(
    show_date: str, database_connection: mysql.connector.connect
) -> Dict[str, Any]:
    """Retrieve show host, scorekeeper and Not My Job guest for the
    requested show ID"""

    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT s.showid, s.bestof, h.host, sk.scorekeeper "
        "FROM ww_showhostmap hm "
        "JOIN ww_hosts h ON h.hostid = hm.hostid "
        "JOIN ww_shows s ON s.showid = hm.showid "
        "JOIN ww_showskmap skm ON skm.showid = hm.showid "
        "JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid "
        "WHERE s.showdate = %s;"
    )
    cursor.execute(query, (show_date,))
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return None

    return {
        "id": result.showid,
        "best_of": bool(result.bestof),
        "host": result.host,
        "scorekeeper": result.scorekeeper,
    }


def retrieve_show_guests(
    show_id: int, database_connection: mysql.connector.connect
) -> List[str]:
    """Retrieves a list of Not My Job guest(s) for the requested show
    ID"""

    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT g.guest "
        "FROM ww_showguestmap gm "
        "JOIN ww_guests g ON g.guestid = gm.guestid "
        "WHERE gm.showid = %s "
        "AND g.guestid <> 76 "
        "ORDER BY gm.showguestmapid ASC;"
    )
    cursor.execute(query, (show_id,))
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    return [row.guest for row in result]


def retrieve_panelists_first_shows(
    database_connection: mysql.connector.connect,
) -> Dict[str, Any]:
    """Returns a dictionary containing all panelists and their
    respective first shows"""

    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT p.panelistid, p.panelist, p.panelistslug, "
        "MIN(s.showdate) AS first, YEAR(MIN(s.showdate)) AS year "
        "FROM ww_showpnlmap pm "
        "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
        "JOIN ww_shows s ON s.showid = pm.showid "
        "WHERE p.panelist <> '<Multiple>' "
        "GROUP BY p.panelist "
        "ORDER BY MIN(s.showdate) ASC;"
    )
    cursor.execute(
        query,
    )
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    panelists = {}
    for row in result:
        show_info = retrieve_show_info(
            show_date=row.first, database_connection=database_connection
        )
        appearance_info = retrieve_appearances_by_panelist(
            panelist_slug=row.panelistslug, database_connection=database_connection
        )

        panelists[row.panelistslug] = {
            "id": row.panelistid,
            "panelist_name": row.panelist,
            "panelist_slug": row.panelistslug,
            "show": row.first.isoformat(),
            "show_id": show_info["id"],
            "year": row.year,
            "best_of": show_info["best_of"],
            "regular_appearances": appearance_info["regular"],
            "host": show_info["host"],
            "scorekeeper": show_info["scorekeeper"],
            "guests": retrieve_show_guests(
                show_id=show_info["id"], database_connection=database_connection
            ),
        }

    return panelists


def panelist_debuts_by_year(
    database_connection: mysql.connector.connect,
) -> Dict[str, Any]:
    """Returns a dictionary of show years with a list of panelists'
    debut information"""

    if not database_connection.is_connected():
        database_connection.reconnect()

    show_years = retrieve_show_years(database_connection=database_connection)
    panelists = retrieve_panelists_first_shows(database_connection=database_connection)

    years_debut = {}
    for year in show_years:
        years_debut[year] = []

    for panelist in panelists:
        panelist_info = panelists[panelist]
        years_debut[panelist_info["year"]].append(panelist_info)

    return years_debut
