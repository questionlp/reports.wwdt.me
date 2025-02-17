# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Scorekeeper Debut by Year Report Functions."""

from typing import Any

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from app.panelists.reports.appearances import retrieve_panelists_by_show_id

from .appearances import retrieve_appearances_by_scorekeeper


def retrieve_show_years(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[int]:
    """Retrieve a list of all show years."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT DISTINCT YEAR(showdate) AS year
        FROM ww_shows
        ORDER BY YEAR(showdate) ASC;
        """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    return [row["year"] for row in result]


def retrieve_show_info(
    show_date: str, database_connection: MySQLConnection | PooledMySQLConnection
) -> dict[str, Any]:
    """Retrieve show host, scorekeeper and Not My Job guest for the requested show ID."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT s.showid, s.bestof, h.host
        FROM ww_showhostmap hm
        JOIN ww_hosts h ON h.hostid = hm.hostid
        JOIN ww_shows s ON s.showid = hm.showid
        WHERE s.showdate = %s;
        """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (show_date,))
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return None

    return {
        "id": result["showid"],
        "best_of": bool(result["bestof"]),
        "host": result["host"],
    }


def retrieve_show_guests(
    show_id: int, database_connection: MySQLConnection | PooledMySQLConnection
) -> list[str]:
    """Retrieves a list of Not My Job guest(s) for the requested show ID."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT g.guest
        FROM ww_showguestmap gm
        JOIN ww_guests g ON g.guestid = gm.guestid
        WHERE gm.showid = %s
        AND g.guestid <> 76
        ORDER BY gm.showguestmapid ASC;
        """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (show_id,))
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    return [row["guest"] for row in result]


def retrieve_scorekeepers_first_shows(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> dict[str, Any]:
    """Returns a dictionary containing all panelists and their first shows."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT sk.scorekeeperid, sk.scorekeeper, sk.scorekeeperslug,
        skm.guest, MIN(s.showdate) AS first,
        YEAR(MIN(s.showdate)) AS year
        FROM ww_showskmap skm
        JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid
        JOIN ww_shows s ON s.showid = skm.showid
        WHERE sk.scorekeeperslug <> 'tbd'
        GROUP BY sk.scorekeeperid, sk.scorekeeperslug, skm.guest
        ORDER BY MIN(s.showdate) ASC;
        """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    hosts = {}
    for row in result:
        show_info = retrieve_show_info(
            show_date=row["first"], database_connection=database_connection
        )
        appearance_info = retrieve_appearances_by_scorekeeper(
            scorekeeper_slug=row["scorekeeperslug"],
            database_connection=database_connection,
        )

        hosts[row["scorekeeperslug"]] = {
            "id": row["scorekeeperid"],
            "scorekeeper_name": row["scorekeeper"],
            "scorekeeper_slug": row["scorekeeperslug"],
            "scorekeeper_guest": bool(row["guest"]),
            "show": row["first"].isoformat(),
            "show_id": show_info["id"],
            "year": row["year"],
            "best_of": show_info["best_of"],
            "regular_appearances": appearance_info["regular"],
            "host": show_info["host"],
            "panelists": retrieve_panelists_by_show_id(
                show_info["id"], database_connection=database_connection
            ),
            "guests": retrieve_show_guests(
                show_id=show_info["id"], database_connection=database_connection
            ),
        }

    return hosts


def scorekeeper_debuts_by_year(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> dict[str, Any]:
    """Returns a dictionary of show years with a list of panelists' debut information."""
    show_years = retrieve_show_years(database_connection=database_connection)
    scorekeepers = retrieve_scorekeepers_first_shows(
        database_connection=database_connection
    )

    years_debut = {}
    for year in show_years:
        years_debut[year] = []

    for scorekeeper in scorekeepers:
        scorekeeper_info = scorekeepers[scorekeeper]
        years_debut[scorekeeper_info["year"]].append(scorekeeper_info)

    return years_debut
