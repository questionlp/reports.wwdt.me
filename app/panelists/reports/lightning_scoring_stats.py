# Copyright (c) 2018-2026 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Panelist Lightning Round Scoring Statistics Report Functions."""

from decimal import Decimal
from typing import Any

import numpy
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from . import common
from .stats_summary import (
    retrieve_all_panelists_stats,
    retrieve_appearances_by_panelist,
)


def retrieve_lightning_start_values_by_panelist(
    panelist_slug: str,
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[Decimal]:
    """Retrieve all Lightning Round starting values for a given panelist."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT pm.panelistlrndstart_decimal FROM ww_showpnlmap pm
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        JOIN ww_shows s ON s.showid = pm.showid
        WHERE p.panelistslug = %s
        AND s.bestof = 0 AND s.repeatshowid IS NULL
        AND pm.panelistlrndstart_decimal IS NOT NULL;
    """
    cursor = database_connection.cursor(dictionary=False)
    cursor.execute(query, (panelist_slug,))
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    return [row[0] for row in result]


def retrieve_lightning_correct_values_by_panelist(
    panelist_slug: str,
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[Decimal]:
    """Retrieve all Lightning Round correct values for a given panelist."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT pm.panelistlrndcorrect_decimal FROM ww_showpnlmap pm
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        JOIN ww_shows s ON s.showid = pm.showid
        WHERE p.panelistslug = %s
        AND s.bestof = 0 AND s.repeatshowid IS NULL
        AND pm.panelistlrndcorrect_decimal IS NOT NULL;
    """
    cursor = database_connection.cursor(dictionary=False)
    cursor.execute(query, (panelist_slug,))
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    return [row[0] for row in result]


def retrieve_lightning_total_scores_by_panelist(
    panelist_slug: str,
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[Decimal]:
    """Retrieve all Lightning Round total scores for a given panelist."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT pm.panelistscore_decimal FROM ww_showpnlmap pm
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        JOIN ww_shows s ON s.showid = pm.showid
        WHERE p.panelistslug = %s
        AND s.bestof = 0 AND s.repeatshowid IS NULL
        AND pm.panelistscore_decimal IS NOT NULL;
    """
    cursor = database_connection.cursor(dictionary=False)
    cursor.execute(query, (panelist_slug,))
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    return [row[0] for row in result]


def retrieve_all_panelists_lightning_scoring_stats(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> dict[str, str | Decimal | None]:
    """Retrieve Lightning Round scoring statistics for all available panelists."""
    panelists = common.retrieve_panelists(database_connection=database_connection)

    if not panelists:
        return None

    _panelists = {}
    for panelist in panelists:
        _slug = panelist["slug"]
        _appearances = retrieve_appearances_by_panelist(
            panelist_slug=_slug, database_connection=database_connection
        )
        _starts = retrieve_lightning_start_values_by_panelist(
            panelist_slug=_slug, database_connection=database_connection
        )
        _corrects = retrieve_lightning_correct_values_by_panelist(
            panelist_slug=_slug, database_connection=database_connection
        )
        _totals = retrieve_lightning_total_scores_by_panelist(
            panelist_slug=_slug, database_connection=database_connection
        )

        if _starts:
            _starts_stats = {
                "count": len(_starts),
                "minimum": Decimal(numpy.amin(_starts)),
                "maximum": Decimal(numpy.amax(_starts)),
                "mean": round(Decimal(numpy.mean(_starts)), 5),
                "median": Decimal(numpy.median(_starts)),
                "standard_deviation": round(Decimal(numpy.std(_starts)), 5),
                "sum": Decimal(numpy.sum(_starts)),
            }
        else:
            _starts_stats = None

        if _corrects:
            _corrects_stats = {
                "count": len(_corrects),
                "minimum": Decimal(numpy.amin(_corrects)),
                "maximum": Decimal(numpy.amax(_corrects)),
                "mean": round(Decimal(numpy.mean(_corrects)), 5),
                "median": Decimal(numpy.median(_corrects)),
                "standard_deviation": round(Decimal(numpy.std(_corrects)), 5),
                "sum": Decimal(numpy.sum(_corrects)),
            }
        else:
            _corrects_stats = None

        if _totals:
            _totals_stats = {
                "count": len(_totals),
                "minimum": Decimal(numpy.amin(_totals)),
                "maximum": Decimal(numpy.amax(_totals)),
                "mean": round(Decimal(numpy.mean(_totals)), 5),
                "median": Decimal(numpy.median(_totals)),
                "standard_deviation": round(Decimal(numpy.std(_totals)), 5),
                "sum": Decimal(numpy.sum(_totals)),
            }
        else:
            _totals_stats = None

        _panelists[panelist["slug"]] = {
            "slug": panelist["slug"],
            "name": panelist["name"],
            "appearances": {
                "regular": _appearances and _appearances.get("regular", None),
                "with_scores": _appearances and _appearances.get("with_scores", None),
            },
            "start_stats": _starts_stats,
            "correct_stats": _corrects_stats,
            "total_stats": _totals_stats,
        }

    return _panelists
