# Copyright (c) 2018-2026 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Scorekeeper Appearances by Year Report Functions."""

from typing import Any

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from app.panelists.reports.appearances_by_year import retrieve_all_years


def retrieve_appearance_counts_by_year(
    year: int, database_connection: MySQLConnection | PooledMySQLConnection
) -> dict[str, dict[str, str | int | None]]:
    """Retrieve scorekeeper appearance counts for a given year."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    all_query = """
        SELECT sk.scorekeeperid, sk.scorekeeper, sk.scorekeeperslug,
        COUNT(sk.scorekeeperid) AS count
        FROM ww_showskmap skm
        JOIN ww_shows s ON s.showid = skm.showid
        JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid
        WHERE YEAR(s.showdate) = %s AND sk.scorekeeperslug <> 'tbd'
        GROUP BY sk.scorekeeperid, sk.scorekeeper, sk.scorekeeperslug
        ORDER BY COUNT(sk.scorekeeperid) DESC, sk.scorekeeper ASC;
    """
    all_cursor = database_connection.cursor(dictionary=True)
    all_cursor.execute(all_query, (year,))
    all_results = all_cursor.fetchall()
    all_cursor.close()

    if not all_results:
        return None

    regular_query = """
        SELECT sk.scorekeeperid, sk.scorekeeper, sk.scorekeeperslug,
        COUNT(sk.scorekeeperid) AS count
        FROM ww_showskmap skm
        JOIN ww_shows s ON s.showid = skm.showid
        JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid
        WHERE YEAR(s.showdate) = %s AND s.bestof = 0
        AND s.repeatshowid IS NULL AND sk.scorekeeperslug <> 'tbd'
        GROUP BY sk.scorekeeperid, sk.scorekeeper, sk.scorekeeperslug
        ORDER BY COUNT(sk.scorekeeperid) DESC, sk.scorekeeper ASC;
    """
    regular_cursor = database_connection.cursor(dictionary=True)
    regular_cursor.execute(regular_query, (year,))
    regular_results = regular_cursor.fetchall()
    regular_cursor.close()

    best_ofs_query = """
        SELECT sk.scorekeeperid, sk.scorekeeper, sk.scorekeeperslug,
        COUNT(sk.scorekeeperid) AS count
        FROM ww_showskmap skm
        JOIN ww_shows s ON s.showid = skm.showid
        JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid
        WHERE YEAR(s.showdate) = %s AND s.bestof = 1
        AND s.repeatshowid IS NULL AND sk.scorekeeperslug <> 'tbd'
        GROUP BY sk.scorekeeperid, sk.scorekeeper, sk.scorekeeperslug
        ORDER BY COUNT(sk.scorekeeperid) DESC, sk.scorekeeper ASC;
    """
    best_ofs_cursor = database_connection.cursor(dictionary=True)
    best_ofs_cursor.execute(best_ofs_query, (year,))
    best_ofs_results = best_ofs_cursor.fetchall()
    best_ofs_cursor.close()

    repeat_best_ofs_query = """
        SELECT sk.scorekeeperid, sk.scorekeeper, sk.scorekeeperslug,
        COUNT(sk.scorekeeperid) AS count
        FROM ww_showskmap skm
        JOIN ww_shows s ON s.showid = skm.showid
        JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid
        WHERE YEAR(s.showdate) = %s AND s.bestof = 1
        AND s.repeatshowid IS NOT NULL AND sk.scorekeeperslug <> 'tbd'
        GROUP BY sk.scorekeeperid, sk.scorekeeper, sk.scorekeeperslug
        ORDER BY COUNT(sk.scorekeeperid) DESC, sk.scorekeeper ASC;
    """
    repeat_best_ofs_cursor = database_connection.cursor(dictionary=True)
    repeat_best_ofs_cursor.execute(repeat_best_ofs_query, (year,))
    repeat_best_ofs_results = repeat_best_ofs_cursor.fetchall()
    repeat_best_ofs_cursor.close()

    repeats_query = """
        SELECT sk.scorekeeperid, sk.scorekeeper, sk.scorekeeperslug,
        COUNT(sk.scorekeeperid) AS count
        FROM ww_showskmap skm
        JOIN ww_shows s ON s.showid = skm.showid
        JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid
        WHERE YEAR(s.showdate) = %s AND s.bestof = 0
        AND s.repeatshowid IS NULL AND sk.scorekeeperslug <> 'tbd'
        GROUP BY sk.scorekeeperid, sk.scorekeeper, sk.scorekeeperslug
        ORDER BY COUNT(sk.scorekeeperid) DESC, sk.scorekeeper ASC;
    """
    repeats_cursor = database_connection.cursor(dictionary=True)
    repeats_cursor.execute(repeats_query, (year,))
    repeats_results = repeats_cursor.fetchall()
    repeats_cursor.close()

    _appearances = {}
    for row in all_results:
        _appearances[row["scorekeeperslug"]] = {
            "name": row["scorekeeper"],
            "slug": row["scorekeeperslug"],
            "regular": 0,
            "best_ofs": 0,
            "repeat_best_ofs": 0,
            "repeats": 0,
            "all": row["count"],
        }

    for row in regular_results:
        _appearances[row["scorekeeperslug"]]["regular"] = row["count"]

    for row in best_ofs_results:
        _appearances[row["scorekeeperslug"]]["best_ofs"] = row["count"]

    for row in repeat_best_ofs_results:
        _appearances[row["scorekeeperslug"]]["repeat_best_ofs"] = row["count"]

    for row in repeats_results:
        _appearances[row["scorekeeperslug"]]["repeats"] = row["count"]

    return _appearances


def retrieve_scorekeeper_appearance_counts(
    scorekeeper_id: int, database_connection: MySQLConnection | PooledMySQLConnection
) -> list[dict[str | int, int]]:
    """Retrieve yearly appearance counts for a given scorekeeper ID.

    Appearance counts exclude both Best Of and repeat shows.
    """
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT YEAR(s.showdate) AS year, COUNT(sk.scorekeeper) AS count
        FROM ww_showskmap skm
        JOIN ww_shows s ON s.showid = skm.showid
        JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid
        WHERE skm.scorekeeperid = %s AND s.bestof = 0
        AND s.repeatshowid IS NULL
        GROUP BY sk.scorekeeper, YEAR(s.showdate)
        ORDER BY sk.scorekeeper ASC, YEAR(s.showdate) ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (scorekeeper_id,))
    results = cursor.fetchall()
    cursor.close()

    if not results:
        return None

    _appearances = {}
    total_appearances = 0
    for row in results:
        _appearances[row["year"]] = row["count"]
        total_appearances += row["count"]

    _appearances["total"] = total_appearances
    return _appearances


def retrieve_scorekeeper_appearance_counts_all(
    scorekeeper_id: int, database_connection: MySQLConnection | PooledMySQLConnection
) -> list[dict[str | int, int]]:
    """Retrieve yearly appearance counts for a given scorekeeper ID.

    Appearance counts include both Best Of and repeat shows.
    """
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT YEAR(s.showdate) AS year, COUNT(sk.scorekeeper) AS count
        FROM ww_showskmap skm
        JOIN ww_shows s ON s.showid = skm.showid
        JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid
        WHERE skm.scorekeeperid = %s
        GROUP BY sk.scorekeeper, YEAR(s.showdate)
        ORDER BY sk.scorekeeper ASC, YEAR(s.showdate) ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (scorekeeper_id,))
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
    """Retrieve all appearance counts for all scorekeepers from the database."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT DISTINCT sk.scorekeeperid, sk.scorekeeper, sk.scorekeeperslug
        FROM ww_showskmap skm
        JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid
        JOIN ww_shows s ON s.showid = skm.showid
        WHERE s.bestof = 0 AND s.repeatshowid IS NULL
        AND sk.scorekeeperslug <> 'tbd'
        ORDER BY sk.scorekeeper ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    _scorekeepers = []
    for row in result:
        scorekeeper_id = row["scorekeeperid"]
        _scorekeepers.append(
            {
                "name": row["scorekeeper"],
                "slug": row["scorekeeperslug"],
                "regular_appearances": retrieve_scorekeeper_appearance_counts(
                    scorekeeper_id=scorekeeper_id,
                    database_connection=database_connection,
                ),
                "all_appearances": retrieve_scorekeeper_appearance_counts_all(
                    scorekeeper_id=scorekeeper_id,
                    database_connection=database_connection,
                ),
            }
        )

    return _scorekeepers


def retrieve_all_appearance_counts_by_year(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> dict[int, dict[str, str | int | None]]:
    """Retrieve all appearance counts for all scorekeepers from the database."""
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
