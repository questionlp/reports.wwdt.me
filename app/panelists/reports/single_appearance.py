# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Panelist Single Appearance Report Functions"""
from typing import Any, Dict, List
import mysql.connector


def retrieve_single_appearances(
    database_connection: mysql.connector.connect,
) -> List[Dict[str, Any]]:
    """Retrieve a list of panelists that have only made a single
    appearance on the show"""

    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT p.panelist, p.panelistslug, s.showdate, "
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
        "ORDER BY p.panelist ASC;"
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
                "appearance": row.showdate.isoformat(),
                "score": row.panelistscore,
                "rank": row.showpnlrank,
            }
        )

    return panelists
