# Copyright (c) 2018-2026 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""On This Day Shows module for Wait Wait Reports."""

from datetime import date
from decimal import Decimal
from typing import Any

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from app.hosts.reports.appearances import retrieve_hosts
from app.panelists.reports.common import retrieve_panelists
from app.scorekeepers.reports.appearances import retrieve_scorekeepers


def retrieve_host_debuts_by_month_day(
    month: int, day: int, database_connection: MySQLConnection | PooledMySQLConnection
) -> list[dict[str, str | bool]] | None:
    """Retrieve host debuts for a given month and day."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    _list_hosts: list[dict[str, str]] = retrieve_hosts(
        database_connection=database_connection
    )
    if not _list_hosts:
        return None

    _hosts_details: list = []
    for _host in _list_hosts:
        query = """
            SELECT s.showdate, s.bestof, s.repeatshowid, hm.guest
            FROM ww_showhostmap hm
            JOIN ww_shows s ON s.showid = hm.showid
            WHERE hm.hostid = %s
            ORDER BY s.showdate ASC
            LIMIT 1;
        """
        cursor = database_connection.cursor(dictionary=True)
        cursor.execute(query, (_host["id"],))
        result_app = cursor.fetchone()
        cursor.close()

        if result_app:
            _date: date = result_app["showdate"]
            if _date.month == month and _date.day == day:
                _hosts_details.append(
                    {
                        "name": _host["name"],
                        "slug": _host["slug"],
                        "show_date": result_app["showdate"].isoformat(),
                        "best_of": bool(result_app["bestof"]),
                        "repeat": bool(result_app["repeatshowid"]),
                        "guest": bool(result_app["guest"]),
                    }
                )

    return _hosts_details


def retrieve_panelist_debuts_by_month_day(
    month: int, day: int, database_connection: MySQLConnection | PooledMySQLConnection
) -> list[dict[str, str | int | bool | Decimal]] | None:
    """Retrieve panelist debuts for a given month and day."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    _list_panelists: list[dict[str, Any]] = retrieve_panelists(
        database_connection=database_connection
    )
    if not _list_panelists:
        return None

    _panelists_details: list = []
    for _panelist in _list_panelists:
        query = """
            SELECT s.showdate, s.bestof, s.repeatshowid,
            pm.panelistlrndstart_decimal, pm.panelistlrndcorrect_decimal,
            pm.panelistscore_decimal, pm.showpnlrank
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE pm.panelistid = %s
            ORDER BY s.showdate ASC
            LIMIT 1;
        """
        cursor = database_connection.cursor(dictionary=True)
        cursor.execute(query, (_panelist["id"],))
        result_app = cursor.fetchone()
        cursor.close()

        if result_app:
            _date: date = result_app["showdate"]
            if _date.month == month and _date.day == day:
                _panelists_details.append(
                    {
                        "name": _panelist["name"],
                        "slug": _panelist["slug"],
                        "show_date": result_app["showdate"].isoformat(),
                        "best_of": bool(result_app["bestof"]),
                        "repeat": bool(result_app["repeatshowid"]),
                        "start": result_app["panelistlrndstart_decimal"],
                        "correct": result_app["panelistlrndcorrect_decimal"],
                        "score": result_app["panelistscore_decimal"],
                        "rank": result_app["showpnlrank"],
                    }
                )

    return _panelists_details


def retrieve_scorekeeper_debuts_by_month_day(
    month: int, day: int, database_connection: MySQLConnection | PooledMySQLConnection
) -> list[dict[str, str | bool]] | None:
    """Retrieve scorekeeper debuts for a given month and day."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    _list_scorekeepers: list[dict[str, str]] = retrieve_scorekeepers(
        database_connection=database_connection
    )
    if not _list_scorekeepers:
        return None

    _scorekeepers_details: list = []
    for _host in _list_scorekeepers:
        query = """
            SELECT s.showdate, s.bestof, s.repeatshowid, skm.guest
            FROM ww_showskmap skm
            JOIN ww_shows s ON s.showid = skm.showid
            WHERE skm.scorekeeperid = %s
            ORDER BY s.showdate ASC
            LIMIT 1;
        """
        cursor = database_connection.cursor(dictionary=True)
        cursor.execute(query, (_host["id"],))
        result_app = cursor.fetchone()
        cursor.close()

        if result_app:
            _date: date = result_app["showdate"]
            if _date.month == month and _date.day == day:
                _scorekeepers_details.append(
                    {
                        "name": _host["name"],
                        "slug": _host["slug"],
                        "show_date": result_app["showdate"].isoformat(),
                        "best_of": bool(result_app["bestof"]),
                        "repeat": bool(result_app["repeatshowid"]),
                        "guest": bool(result_app["guest"]),
                    }
                )

    return _scorekeepers_details
