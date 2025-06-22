# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Panelist Statistics Summary Report Functions."""

from decimal import Decimal
from typing import Any

import numpy
from flask import current_app
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from . import common


def retrieve_appearances_by_panelist(
    panelist_slug: str,
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> dict[str, int]:
    """Retrieve appearance data for the requested panelist by the panelist's slug string."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT (
        SELECT COUNT(pm.showid) FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        WHERE s.bestof = 0 AND s.repeatshowid IS NULL AND
        p.panelistslug = %s ) AS regular, (
        SELECT COUNT(pm.showid) FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        WHERE p.panelistslug = %s ) AS all_shows, (
        SELECT COUNT(pm.panelistid) FROM ww_showpnlmap pm
        JOIN ww_shows s ON pm.showid = s.showid
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        WHERE p.panelistslug = %s AND s.bestof = 0 AND
        s.repeatshowid IS NULL
        AND pm.panelistscore_decimal IS NOT NULL )
        AS with_scores;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(
        query,
        (
            panelist_slug,
            panelist_slug,
            panelist_slug,
        ),
    )
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return None

    return {
        "regular": result["regular"],
        "all": result["all_shows"],
        "with_scores": result["with_scores"],
    }


def retrieve_scores_by_panelist(
    panelist_slug: str,
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[int]:
    """Retrieve all scores for the requested panelist by the panelist's slug string."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT pm.panelistscore_decimal FROM ww_showpnlmap pm
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        JOIN ww_shows s ON s.showid = pm.showid
        WHERE s.bestof = 0 AND s.repeatshowid IS NULL
        AND p.panelistslug = %s
        AND pm.panelistscore_decimal IS NOT NULL;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (panelist_slug,))
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    return [row["panelistscore_decimal"] for row in result]


def retrieve_all_panelists_stats(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> dict[str, Any]:
    """Retrieve common statistics for all available panelists."""
    panelists = common.retrieve_panelists(database_connection=database_connection)

    if not panelists:
        return None

    all_stats = {}

    for panelist in panelists:
        panelist_slug = panelist["slug"]
        all_stats[panelist_slug] = {
            "appearances": retrieve_appearances_by_panelist(
                panelist_slug=panelist_slug,
                database_connection=database_connection,
            ),
        }

        scores = retrieve_scores_by_panelist(
            panelist_slug=panelist_slug,
            database_connection=database_connection,
        )
        if scores:
            all_stats[panelist_slug]["stats"] = {
                "minimum": Decimal(numpy.amin(scores)),
                "maximum": Decimal(numpy.amax(scores)),
                "mean": round(Decimal(numpy.mean(scores)), 5),
                "median": Decimal(numpy.median(scores)),
                "standard_deviation": round(Decimal(numpy.std(scores)), 5),
                "total": Decimal(numpy.sum(scores)),
            }
        else:
            all_stats[panelist_slug]["stats"] = None

    return all_stats
