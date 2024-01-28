# Copyright (c) 2018-2024 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Scorekeeper Introductions Report Functions."""
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection


def retrieve_scorekeepers_with_introductions(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict]:
    """Retrieve a list of scorekeepers that have show introduction entries in the database."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT DISTINCT sk.scorekeeperid, sk.scorekeeper, "
        "sk.scorekeeperslug "
        "FROM ww_showskmap skm "
        "JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid "
        "WHERE skm.description IS NOT NULL "
        "ORDER BY sk.scorekeeper ASC;"
    )
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    scorekeepers = []
    for row in result:
        scorekeepers.append(
            {
                "id": row.scorekeeperid,
                "name": row.scorekeeper,
                "slug": row.scorekeeperslug,
            }
        )

    return scorekeepers


def retrieve_all_scorekeeper_introductions(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> dict:
    """Retrieve all scorekeeper introductions from the database."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    scorekeepers = retrieve_scorekeepers_with_introductions(
        database_connection=database_connection
    )
    all_introductions = {}

    cursor = database_connection.cursor(named_tuple=True)
    for scorekeeper in scorekeepers:
        scorekeeper_intros = []
        query = (
            "SELECT s.showid, s.showdate, s.bestof, s.repeatshowid, "
            "skm.description "
            "FROM ww_showskmap skm "
            "JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid "
            "JOIN ww_shows s ON s.showid = skm.showid "
            "WHERE sk.scorekeeperid = %s "
            "AND skm.description IS NOT NULL "
            "ORDER BY s.showdate ASC;"
        )
        cursor.execute(query, (scorekeeper["id"],))
        result = cursor.fetchall()

        if result:
            for row in result:
                scorekeeper_intros.append(
                    {
                        "id": row.showid,
                        "date": row.showdate.isoformat(),
                        "best_of": bool(row.bestof),
                        "repeat_show": bool(row.repeatshowid),
                        "introduction": row.description,
                    }
                )

        all_introductions[scorekeeper["id"]] = scorekeeper_intros

    cursor.close()
    return all_introductions
