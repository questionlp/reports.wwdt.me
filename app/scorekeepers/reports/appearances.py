# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Scorekeeper Appearances Report Functions."""
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection


def retrieve_all_scorekeepers(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict]:
    """Retrieves a dictionary for all available scorekeepers from the database."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(dictionary=True)
    query = """
        SELECT sk.scorekeeperid, sk.scorekeeper, sk.scorekeeperslug
        FROM ww_scorekeepers sk
        WHERE sk.scorekeeper <> '(TBD)'
        ORDER BY sk.scorekeeperslug ASC;
        """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    scorekeepers = []
    for row in result:
        scorekeepers.append(
            {
                "name": row["scorekeeper"],
                "slug": row["scorekeeperslug"],
            }
        )

    return scorekeepers


def retrieve_appearances_by_scorekeeper(
    scorekeeper_slug: str, database_connection: MySQLConnection | PooledMySQLConnection
) -> dict:
    """Retrieve appearance data for the requested scorekeeper."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(dictionary=True)
    query = """
        SELECT (
        SELECT COUNT(skm.showid) FROM ww_showskmap skm
        JOIN ww_shows s ON s.showid = skm.showid
        JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid
        WHERE s.bestof = 0 AND s.repeatshowid IS NULL AND
        sk.scorekeeperslug = %s ) AS regular, (
        SELECT COUNT(skm.showid) FROM ww_showskmap skm
        JOIN ww_shows s ON s.showid = skm.showid
        JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid
        WHERE sk.scorekeeperslug = %s ) AS allshows;
        """
    cursor.execute(
        query,
        (
            scorekeeper_slug,
            scorekeeper_slug,
        ),
    )
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return {
            "regular": None,
            "all": None,
        }

    return {
        "regular": result["regular"],
        "all": result["allshows"],
    }


def retrieve_first_most_recent_appearances(
    scorekeeper_slug: str, database_connection: MySQLConnection | PooledMySQLConnection
) -> dict:
    """Retrieve a scorekeeper's first and most recent appearances for both regular and all shows."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(dictionary=True)
    query = """
        SELECT MIN(s.showdate) AS min, MAX(s.showdate) AS max
        FROM ww_showskmap skm
        JOIN ww_shows s ON s.showid = skm.showid
        JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid
        WHERE sk.scorekeeperslug = %s
        AND s.bestof = 0
        AND s.repeatshowid IS null;
        """
    cursor.execute(query, (scorekeeper_slug,))
    result = cursor.fetchone()

    if not result:
        return None

    first = result["min"].isoformat() if result["min"] else None
    most_recent = result["max"].isoformat() if result["max"] else None

    query = """
        SELECT MIN(s.showdate) AS min, MAX(s.showdate) AS max
        FROM ww_showskmap skm
        JOIN ww_shows s ON s.showid = skm.showid
        JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid
        WHERE sk.scorekeeperslug = %s;
        """
    cursor.execute(query, (scorekeeper_slug,))
    result_all = cursor.fetchone()
    cursor.close()

    if not result_all:
        return {
            "first": first,
            "most_recent": most_recent,
            "first_all": None,
            "most_recent_all": None,
        }

    first_all = result_all["min"].isoformat() if result_all["min"] else None
    most_recent_all = result_all["max"].isoformat() if result_all["max"] else None

    return {
        "first": first,
        "most_recent": most_recent,
        "first_all": first_all,
        "most_recent_all": most_recent_all,
    }


def retrieve_appearance_summaries(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict]:
    """Retrieve scorekeeper appearance summary.

    Returned summary includes appearance counts, and first and most
    recent appearances.
    """
    scorekeepers = retrieve_all_scorekeepers(database_connection)

    if not scorekeepers:
        return None

    scorekeepers_summary = {}
    for scorekeeper in scorekeepers:
        appearance_count = retrieve_appearances_by_scorekeeper(
            scorekeeper["slug"], database_connection
        )
        first_most_recent = retrieve_first_most_recent_appearances(
            scorekeeper["slug"], database_connection
        )
        scorekeepers_summary[scorekeeper["slug"]] = {
            "slug": scorekeeper["slug"],
            "name": scorekeeper["name"],
            "regular_shows": appearance_count["regular"],
            "all_shows": appearance_count["all"],
            "first": first_most_recent["first"],
            "first_all": first_most_recent["first_all"],
            "most_recent": first_most_recent["most_recent"],
            "most_recent_all": first_most_recent["most_recent_all"],
        }

    return scorekeepers_summary
