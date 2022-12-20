# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Panelist First Appearance Wins"""
from typing import Dict, List, Union

from flask import current_app
import mysql.connector


def retrieve_panelists_first_appearance_wins(
    database_connection: mysql.connector.connect,
) -> Dict[str, Union[str, int]]:
    """Returns a dictionary containing panelists that have won first
    place or were tied for first place on their first appearance."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT DISTINCT p.panelistslug "
        "FROM ww_showpnlmap pm "
        "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
        "JOIN ww_shows s ON s.showid = pm.showid "
        "WHERE s.bestof = 0 "
        "AND s.repeatshowid IS NULL "
        "AND pm.showpnlrank IN ('1', '1t') "
        "ORDER BY p.panelistslug;"
    )

    cursor.execute(
        query,
    )
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    panelist_slugs = [panelist.panelistslug for panelist in result]

    panelists = {}
    for panelist_slug in panelist_slugs:
        cursor = database_connection.cursor(named_tuple=True)
        query = (
            "SELECT p.panelist, s.showid, s.showdate, pm.panelistlrndstart, "
            "pm.panelistlrndcorrect, pm.panelistscore, pm.showpnlrank "
            "FROM ww_showpnlmap pm "
            "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
            "JOIN ww_shows s ON s.showid = pm.showid "
            "WHERE p.panelistslug = %s "
            "AND s.bestof = 0 AND s.repeatshowid IS NULL "
            "ORDER BY s.showdate ASC "
            "LIMIT 1;"
        )
        cursor.execute(query, (panelist_slug,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            if result.showpnlrank == "1" or result.showpnlrank == "1t":
                panelists[panelist_slug] = {
                    "name": result.panelist,
                    "show_date": result.showdate.isoformat(),
                    "start": result.panelistlrndstart,
                    "correct": result.panelistlrndcorrect,
                    "score": result.panelistscore,
                    "rank": result.showpnlrank,
                }

    return panelists
