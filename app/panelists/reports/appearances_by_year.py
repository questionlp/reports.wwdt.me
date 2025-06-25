# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Panelist Appearances by Year Report Functions."""

from typing import Any

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection


def retrieve_appearance_counts_by_year(
    year: int, database_connection: MySQLConnection | PooledMySQLConnection
) -> dict[str, dict[str, str | int | None]]:
    """Retrieve panelist appearance counts for a given year."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    all_query = """
        SELECT p.panelistid, p.panelist, p.panelistslug,
        COUNT(p.panelistid) AS count
        FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        WHERE YEAR(s.showdate) = %s
        AND p.panelistslug <> 'multiple'
        GROUP BY p.panelistid, p.panelist, p.panelistslug
        ORDER BY COUNT(p.panelistid) DESC, p.panelist ASC;
    """
    all_cursor = database_connection.cursor(dictionary=True)
    all_cursor.execute(all_query, (year,))
    all_results = all_cursor.fetchall()
    all_cursor.close()

    if not all_results:
        return None

    regular_query = """
        SELECT p.panelistid, p.panelist, p.panelistslug,
        COUNT(p.panelistid) AS count
        FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        WHERE YEAR(s.showdate) = %s AND s.bestof = 0
        AND s.repeatshowid IS NULL
        AND p.panelistslug <> 'multiple'
        GROUP BY p.panelistid, p.panelist, p.panelistslug
        ORDER BY COUNT(p.panelistid) DESC, p.panelist ASC;
    """
    regular_cursor = database_connection.cursor(dictionary=True)
    regular_cursor.execute(regular_query, (year,))
    regular_results = regular_cursor.fetchall()
    regular_cursor.close()

    best_ofs_query = """
        SELECT p.panelistid, p.panelist, p.panelistslug,
        COUNT(p.panelistid) AS count
        FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        WHERE YEAR(s.showdate) = %s AND s.bestof = 1
        AND s.repeatshowid IS NULL
        AND p.panelistslug <> 'multiple'
        GROUP BY p.panelistid, p.panelist, p.panelistslug
        ORDER BY COUNT(p.panelistid) DESC, p.panelist ASC;
    """
    best_ofs_cursor = database_connection.cursor(dictionary=True)
    best_ofs_cursor.execute(best_ofs_query, (year,))
    best_ofs_results = best_ofs_cursor.fetchall()
    best_ofs_cursor.close()

    repeat_best_ofs_query = """
        SELECT p.panelistid, p.panelist, p.panelistslug,
        COUNT(p.panelistid) AS count
        FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        WHERE YEAR(s.showdate) = %s AND s.bestof = 1
        AND s.repeatshowid IS NOT NULL
        AND p.panelistslug <> 'multiple'
        GROUP BY p.panelistid, p.panelist, p.panelistslug
        ORDER BY COUNT(p.panelistid) DESC, p.panelist ASC;
    """
    repeat_best_ofs_cursor = database_connection.cursor(dictionary=True)
    repeat_best_ofs_cursor.execute(repeat_best_ofs_query, (year,))
    repeat_best_ofs_results = repeat_best_ofs_cursor.fetchall()
    repeat_best_ofs_cursor.close()

    repeats_query = """
        SELECT p.panelistid, p.panelist, p.panelistslug,
        COUNT(p.panelistid) AS count
        FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        WHERE YEAR(s.showdate) = %s AND s.bestof = 0
        AND s.repeatshowid IS NOT NULL
        AND p.panelistslug <> 'multiple'
        GROUP BY p.panelistid, p.panelist, p.panelistslug
        ORDER BY COUNT(p.panelistid) DESC, p.panelist ASC;
    """
    repeats_cursor = database_connection.cursor(dictionary=True)
    repeats_cursor.execute(repeats_query, (year,))
    repeats_results = repeats_cursor.fetchall()
    repeats_cursor.close()

    _appearances = {}
    for row in all_results:
        _appearances[row["panelistslug"]] = {
            "name": row["panelist"],
            "slug": row["panelistslug"],
            "regular": 0,
            "best_ofs": 0,
            "repeat_best_ofs": 0,
            "repeats": 0,
            "all": row["count"],
        }

    for row in regular_results:
        _appearances[row["panelistslug"]]["regular"] = row["count"]

    for row in best_ofs_results:
        _appearances[row["panelistslug"]]["best_ofs"] = row["count"]

    for row in repeat_best_ofs_results:
        _appearances[row["panelistslug"]]["repeat_best_ofs"] = row["count"]

    for row in repeats_results:
        _appearances[row["panelistslug"]]["repeats"] = row["count"]

    return _appearances


def retrieve_panelist_appearance_counts(
    panelist_id: int, database_connection: MySQLConnection | PooledMySQLConnection
) -> list[dict[str | int, int]]:
    """Retrieve yearly appearance counts for a given panelist ID.

    Appearance counts exclude both Best Of and repeat shows.
    """
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT YEAR(s.showdate) AS year, COUNT(p.panelist) AS count
        FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        WHERE pm.panelistid = %s AND s.bestof = 0
        AND s.repeatshowid IS NULL
        GROUP BY p.panelist, YEAR(s.showdate)
        ORDER BY p.panelist ASC, YEAR(s.showdate) ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (panelist_id,))
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    _appearances = {}
    total_appearances = 0
    for row in result:
        _appearances[row["year"]] = row["count"]
        total_appearances += row["count"]

    _appearances["total"] = total_appearances
    return _appearances


def retrieve_panelist_appearance_counts_all(
    panelist_id: int, database_connection: MySQLConnection | PooledMySQLConnection
) -> list[dict[str | int, int]]:
    """Retrieve yearly appearance counts for a given panelist ID.

    Appearance counts include both Best Of and repeat shows.
    """
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT YEAR(s.showdate) AS year, COUNT(p.panelist) AS count
        FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        WHERE pm.panelistid = %s
        GROUP BY p.panelist, YEAR(s.showdate)
        ORDER BY p.panelist ASC, YEAR(s.showdate) ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (panelist_id,))
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    _appearances = {}
    total_appearances = 0
    for row in result:
        _appearances[row["year"]] = row["count"]
        total_appearances += row["count"]

    _appearances["total"] = total_appearances
    return _appearances


def retrieve_all_appearance_counts(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict[str, Any]]:
    """Retrieve all appearance counts for all panelists from the database."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT DISTINCT p.panelistid, p.panelist, p.panelistslug
        FROM ww_showpnlmap pm
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        JOIN ww_shows s ON s.showid = pm.showid
        WHERE s.bestof = 0 AND s.repeatshowid IS NULL
        ORDER BY p.panelist ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    _panelists = []
    for row in result:
        panelist_id = row["panelistid"]
        _panelists.append(
            {
                "name": row["panelist"],
                "slug": row["panelistslug"],
                "regular_appearances": retrieve_panelist_appearance_counts(
                    panelist_id=panelist_id, database_connection=database_connection
                ),
                "all_appearances": retrieve_panelist_appearance_counts_all(
                    panelist_id=panelist_id, database_connection=database_connection
                ),
            }
        )

    return _panelists


def retrieve_all_appearance_counts_by_year(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> dict[int, dict[str, str | int | None]]:
    """Retrieve all appearance counts for all panelists from the database."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    _years_list = retrieve_all_years(database_connection=database_connection)

    if not _years_list:
        return None

    _years = {}
    for _year in _years_list:
        _appearances = retrieve_appearance_counts_by_year(
            year=_year, database_connection=database_connection
        )

        if _appearances:
            _years[_year] = _appearances
        else:
            _years[_year] = None

    return _years


def retrieve_all_years(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[int]:
    """Retrieve a list of all available show years."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(dictionary=True)
    query = """
        SELECT DISTINCT YEAR(s.showdate) AS year FROM ww_shows s
        ORDER BY YEAR(s.showdate) ASC;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    return [row["year"] for row in result]
