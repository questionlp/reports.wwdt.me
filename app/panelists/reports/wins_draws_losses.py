# Copyright (c) 2018-2026 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Panelist Wins Report Functions."""

from decimal import Decimal

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from . import common

table_columns: dict[str, str] = {
    "panelist": "Panelist",
    "wins": "Wins",
    "wins_percent": "Win %",
    "draws": "Draws",
    "draws_percent": "Draw %",
    "losses": "Losses",
    "losses_percent": "Loss %",
    "total": "Total",
}

form_minimum_values: list[int] = [5, 10, 15, 20]


def retrieve_panelist_wins_draws_losses(
    panelist_id: int,
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> dict[str, int]:
    """Retrieve wins, draws, losses and total counts for a given panelist."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT (
            SELECT COUNT(pm.showpnlrank)
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE pm.panelistid = %s
            AND s.bestof = 0 AND s.repeatshowid IS NULL
            AND pm.showpnlrank = '1'
        ) AS 'wins', (
            SELECT COUNT(pm.showpnlrank)
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE pm.panelistid = %s
            AND s.bestof = 0 AND s.repeatshowid IS NULL
            AND pm.showpnlrank = '1t'
        ) AS 'draws', (
            SELECT COUNT(pm.showpnlrank)
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE pm.panelistid = %s
            AND s.bestof = 0 AND s.repeatshowid IS NULL
            AND pm.showpnlrank IN ('2', '2t', '3')
        ) AS 'losses';
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(
        query,
        (
            panelist_id,
            panelist_id,
            panelist_id,
        ),
    )
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return None

    _wins = result["wins"]
    _draws = result["draws"]
    _losses = result["losses"]
    _total = result["wins"] + result["draws"] + result["losses"]

    if _total:
        return {
            "wins": _wins,
            "wins_percent": round(Decimal((_wins / _total) * 100), 5),
            "draws": _draws,
            "draws_percent": round(Decimal((_draws / _total) * 100), 5),
            "losses": _losses,
            "losses_percent": round(Decimal((_losses / _total) * 100), 5),
            "total": _total,
        }

    return None


def retrieve_all_wins_draws_losses(
    database_connection: MySQLConnection | PooledMySQLConnection,
    minimum_total_count: int = 0,
) -> dict[str, str | int | None]:
    """Retrieves wins, draws, losses and total counts for all panelists."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    _panelists = common.retrieve_panelists(database_connection=database_connection)

    if not _panelists:
        return None

    _counts = {}
    for _panelist in _panelists:
        panelist_counts = retrieve_panelist_wins_draws_losses(
            panelist_id=_panelist["id"], database_connection=database_connection
        )

        if panelist_counts and panelist_counts["total"] >= minimum_total_count:
            _counts[_panelist["slug"]] = {
                "name": _panelist["name"],
                "slug": _panelist["slug"],
                "wins": panelist_counts["wins"],
                "wins_percent": panelist_counts["wins_percent"],
                "draws": panelist_counts["draws"],
                "draws_percent": panelist_counts["draws_percent"],
                "losses": panelist_counts["losses"],
                "losses_percent": panelist_counts["losses_percent"],
                "total": panelist_counts["total"],
            }
        else:
            _counts[_panelist["slug"]] = {
                "name": _panelist["name"],
                "slug": _panelist["slug"],
                "wins": 0,
                "wins_percent": Decimal(0),
                "draws": 0,
                "draws_percent": Decimal(0),
                "losses": 0,
                "losses_percent": Decimal(0),
                "total": 0,
            }

    return _counts
