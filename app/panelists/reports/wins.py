# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Panelist Wins Report Functions."""

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection


def retrieve_most_outright_wins_by_year(
    show_year: int, database_connection: MySQLConnection | PooledMySQLConnection
) -> dict[str, str | int] | None:
    """Retrieve panelists with the most outright wins for a given year.

    Does not include Best Of and/or repeat shows. Panelists are sorted
    by number of outright wins in descending order.
    """
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT p.panelist, p.panelistslug, COUNT(pm.showpnlrank) AS wins
        FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        WHERE YEAR(s.showdate) = %s
        AND pm.showpnlrank = '1'
        AND s.bestof = 0 AND s.repeatshowid IS NULL
        GROUP BY p.panelist, p.panelistslug
        ORDER BY COUNT(p.panelistid) DESC, p.panelist ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (show_year,))
    results = cursor.fetchall()

    if not results:
        return None

    _panelists = {}
    for row in results:
        _panelists[row["panelistslug"]] = {
            "name": row["panelist"],
            "slug": row["panelistslug"],
            "wins": row["wins"],
        }

    return _panelists


def retrieve_most_outright_wins_plus_ties_by_year(
    show_year: int, database_connection: MySQLConnection | PooledMySQLConnection
) -> dict[str, str | int] | None:
    """Retrieve panelists with the most outright wins plus ties for first place for a given year.

    Does not include Best Of and/or repeat shows. Panelists are sorted
    by number of outright wins plus ties in descending order.
    """
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT p.panelist, p.panelistslug, COUNT(pm.showpnlrank) AS wins
        FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        WHERE YEAR(s.showdate) = %s
        AND pm.showpnlrank IN ('1', '1t')
        AND s.bestof = 0 AND s.repeatshowid IS NULL
        GROUP BY p.panelist, p.panelistslug
        ORDER BY COUNT(p.panelistid) DESC, p.panelist ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (show_year,))
    results = cursor.fetchall()

    if not results:
        return None

    _panelists = {}
    for row in results:
        _panelists[row["panelistslug"]] = {
            "name": row["panelist"],
            "slug": row["panelistslug"],
            "wins_ties": row["wins"],
        }

    return _panelists


def retrieve_combined_outright_wins_ties_by_year(
    show_year: int, database_connection: MySQLConnection | PooledMySQLConnection
) -> dict[str, str | int] | None:
    """Retrieves a combined dictionary of panelists and counts of wins/ties for a given year.

    Does not include Best Of and/or repeat shows. Panelists are sorted
    by number of outright wins in descending order.
    """
    if not database_connection.is_connected():
        database_connection.reconnect()

    _wins_ties = retrieve_most_outright_wins_plus_ties_by_year(
        show_year=show_year, database_connection=database_connection
    )
    if not _wins_ties:
        return None

    _outright_wins = retrieve_most_outright_wins_by_year(
        show_year=show_year, database_connection=database_connection
    )
    if not _outright_wins:
        return None

    for panelist in _wins_ties:
        if panelist in _outright_wins:
            _outright_wins[panelist]["wins_ties"] = _wins_ties[panelist]["wins_ties"]
        else:
            _outright_wins[panelist] = {
                "name": _wins_ties[panelist]["name"],
                "slug": _wins_ties[panelist]["slug"],
                "wins": 0,
                "wins_ties": _wins_ties[panelist]["wins_ties"],
            }

    return _outright_wins
