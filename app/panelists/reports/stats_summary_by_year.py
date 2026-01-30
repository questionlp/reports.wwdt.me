# Copyright (c) 2018-2026 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Panelist Statistics Summary Report Functions."""

from decimal import Decimal
from typing import Any

import numpy
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from .common import retrieve_panelist_info_by_slug
from .debut_by_year import retrieve_show_years


def retrieve_appearances_by_year(
    panelist_slug: str,
    year: int,
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> dict[str, int]:
    """Retrieve appearance data for a given panelist."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT (
        SELECT COUNT(pm.showid) FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        WHERE p.panelistslug = %s AND YEAR(s.showdate) = %s AND
        s.bestof = 0 AND s.repeatshowid IS NULL) AS regular, (
        SELECT COUNT(pm.showid) FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        WHERE p.panelistslug = %s AND YEAR(s.showdate) = %s) AS all_shows, (
        SELECT COUNT(pm.panelistid) FROM ww_showpnlmap pm
        JOIN ww_shows s ON pm.showid = s.showid
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        WHERE p.panelistslug = %s AND YEAR(s.showdate) = %s
        AND s.bestof = 0 AND s.repeatshowid IS NULL
        AND pm.panelistscore_decimal IS NOT NULL )
        AS with_scores;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(
        query,
        (
            panelist_slug,
            year,
            panelist_slug,
            year,
            panelist_slug,
            year,
        ),
    )
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return None

    if result["regular"] or result["all_shows"] or result["with_scores"]:
        return {
            "regular": result["regular"],
            "all": result["all_shows"],
            "with_scores": result["with_scores"],
        }

    return None


def retrieve_scores_by_year(
    panelist_slug: str,
    year: int,
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[int]:
    """Retrieve all scores for a given panelist."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT pm.panelistscore_decimal FROM ww_showpnlmap pm
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        JOIN ww_shows s ON s.showid = pm.showid
        WHERE p.panelistslug = %s AND YEAR(s.showdate) = %s
        AND s.bestof = 0 AND s.repeatshowid IS NULL
        AND pm.panelistscore_decimal IS NOT NULL;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(
        query,
        (
            panelist_slug,
            year,
        ),
    )
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    return [row["panelistscore_decimal"] for row in result]


def retrieve_all_stats_by_year(
    panelist_slug: str,
    year: int,
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> dict[str, Any]:
    """Retrieve common statistics for a given panelist."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    all_stats = {
        "appearances": retrieve_appearances_by_year(
            panelist_slug=panelist_slug,
            year=year,
            database_connection=database_connection,
        ),
    }

    scores = retrieve_scores_by_year(
        panelist_slug=panelist_slug,
        year=year,
        database_connection=database_connection,
    )
    if scores:
        all_stats["stats"] = {
            "minimum": Decimal(numpy.amin(scores)),
            "maximum": Decimal(numpy.amax(scores)),
            "mean": round(Decimal(numpy.mean(scores)), 5),
            "median": Decimal(numpy.median(scores)),
            "standard_deviation": round(Decimal(numpy.std(scores)), 5),
            "total": Decimal(numpy.sum(scores)),
        }
    else:
        all_stats["stats"] = None

    return all_stats


def retrieve_stats_all_years(
    panelist_slug: str,
    database_connection: MySQLConnection | PooledMySQLConnection,
):
    """Retrieves statistics for all years for a given panelist."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    _info = retrieve_panelist_info_by_slug(
        panelist_slug=panelist_slug, database_connection=database_connection
    )
    if not _info:
        return None

    _years = retrieve_show_years(database_connection=database_connection)

    _stats = {}
    for _year in _years:
        _stats[_year] = retrieve_all_stats_by_year(
            panelist_slug=panelist_slug,
            year=_year,
            database_connection=database_connection,
        )

    _panelist = {"name": _info["name"], "slug": _info["slug"], "statistics": _stats}

    return _panelist
