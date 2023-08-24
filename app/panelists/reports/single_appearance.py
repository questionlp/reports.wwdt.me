# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2023 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Panelist Single Appearance Report Functions"""
from typing import Any, Dict, List

from flask import current_app
import mysql.connector


def retrieve_single_appearances(
    database_connection: mysql.connector.connect, use_decimal_scores: bool = False
) -> List[Dict[str, Any]]:
    """Retrieve a list of panelists that have only made a single
    appearance on the show"""
    if (
        use_decimal_scores
        and not current_app.config["app_settings"]["has_decimal_scores_column"]
    ):
        return None

    if not database_connection.is_connected():
        database_connection.reconnect()

    if use_decimal_scores:
        query = """
            SELECT p.panelist, p.panelistslug, s.showdate,
            pm.panelistscore_decimal AS score, pm.showpnlrank
            FROM ww_showpnlmap pm
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE pm.showpnlmapid IN (
            SELECT ANY_VALUE(pm.showpnlmapid)
            FROM ww_showpnlmap pm
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE s.bestof = 0 AND s.repeatshowid IS NULL
            GROUP BY p.panelist
            HAVING COUNT(p.panelist) = 1 )
            ORDER BY p.panelist ASC;
            """
    else:
        query = """
            SELECT p.panelist, p.panelistslug, s.showdate,
            pm.panelistscore AS score, pm.showpnlrank FROM ww_showpnlmap pm
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE pm.showpnlmapid IN (
            SELECT ANY_VALUE(pm.showpnlmapid)
            FROM ww_showpnlmap pm
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE s.bestof = 0 AND s.repeatshowid IS NULL
            GROUP BY p.panelist
            HAVING COUNT(p.panelist) = 1 )
            ORDER BY p.panelist ASC;
            """
    cursor = database_connection.cursor(named_tuple=True)
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
                "score": row.score,
                "score_decimal" "rank": row.showpnlrank,
            }
        )

    return panelists
