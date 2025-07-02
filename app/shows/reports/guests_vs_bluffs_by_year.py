# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Show Not My Job Guest Wins Rate vs Bluff the Listener Wins Rate by Year Report Functions."""

from typing import Any

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from app.panelists.reports.appearances_by_year import retrieve_all_years


def retrieve_not_my_job_stats_by_year(
    year: int,
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> dict[str, Any]:
    """Returns a dictionary containing Not My Job statistics.

    Returned statistics includes the total number of Not My Job guest
    entries that have a score entered, total number of times a Not My
    Job guest has won (including exceptions), and a total number of
    times a Not My Job guest has lost.
    """
    if not database_connection.is_connected():
        database_connection.reconnect()

    # Get a count of all Not My Job guest entries with scores and are
    # from shows that are not Best Of or repeats
    query = """
        SELECT COUNT(g.guestid)
        FROM ww_showguestmap gm
        JOIN ww_guests g ON g.guestid = gm.guestid
        JOIN ww_shows s ON s.showid = gm.showid
        WHERE YEAR(s.showdate) = %s AND s.bestof = 0
        AND s.repeatshowid IS NULL AND g.guestslug <> 'none'
        AND gm.guestscore IS NOT NULL;
    """
    cursor = database_connection.cursor(dictionary=False)
    cursor.execute(query, (year,))
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return None

    count_all_guest_scores = result[0]

    # Get a count of all Not My Job guest entries in which a guest won
    # outright or was given a win via a scoring exception
    query = """
        SELECT COUNT(g.guestid)
        FROM ww_showguestmap gm
        JOIN ww_guests g ON g.guestid = gm.guestid
        JOIN ww_shows s ON s.showid = gm.showid
        WHERE YEAR(s.showdate) = %s AND s.bestof = 0
        AND s.repeatshowid IS NULL AND g.guestslug <> 'none'
        AND (gm.guestscore >= 2 OR gm.exception = 1);
    """
    cursor = database_connection.cursor(dictionary=False)
    cursor.execute(query, (year,))
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return None

    count_guest_wins = result[0]

    # Get a count of all Not My Job guest entries in which a guest did
    # not win
    query = """
        SELECT COUNT(g.guestid)
        FROM ww_showguestmap gm
        JOIN ww_guests g ON g.guestid = gm.guestid
        JOIN ww_shows s ON s.showid = gm.showid
        WHERE YEAR(s.showdate) = %s AND s.bestof = 0
        AND s.repeatshowid IS NULL AND g.guestslug <> 'none'
        AND (gm.guestscore < 2 AND gm.exception = 0);
    """
    cursor = database_connection.cursor(dictionary=False)
    cursor.execute(query, (year,))
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return None

    count_guest_losses = result[0]

    # Get a list of Not My Job guests that have only appeared on Best Of
    # shows
    query = """
        SELECT DISTINCT g.guestid
        FROM ww_showguestmap gm
        JOIN ww_shows s ON s.showid = gm.showid
        JOIN ww_guests g ON g.guestid = gm.guestid
        WHERE YEAR(s.showdate) = %s AND s.bestof = 1
        AND s.repeatshowid IS NULL
        AND g.guestid NOT IN (
        SELECT gm.guestid
        FROM ww_showguestmap gm
        JOIN ww_shows s ON s.showid = gm.showid
        WHERE s.bestof = 0 AND s.repeatshowid IS NULL );
    """
    cursor = database_connection.cursor(dictionary=False)
    cursor.execute(query, (year,))
    result = cursor.fetchall()
    cursor.close()

    if not result:
        best_of_only_guest_ids = []
        best_of_only_guest_wins = 0
        best_of_only_guest_losses = 0
    else:
        best_of_only_guest_ids = [guest[0] for guest in result]
        best_of_only_guest_wins = 0
        best_of_only_guest_losses = 0

        for guest_id in best_of_only_guest_ids:
            query = """
                SELECT s.showdate, gm.guestscore, gm.exception
                FROM ww_showguestmap gm
                JOIN ww_shows s ON s.showid = gm.showid
                WHERE YEAR(s.showdate) = %s AND s.repeatshowid IS NULL
                AND gm.guestid = %s
                ORDER BY s.showdate ASC
                LIMIT 1;
            """
            cursor = database_connection.cursor(dictionary=True)
            cursor.execute(
                query,
                (
                    year,
                    guest_id,
                ),
            )
            result = cursor.fetchone()
            cursor.close()

            if result:
                if result["guestscore"] >= 2 or bool(result["exception"]):
                    best_of_only_guest_wins += 1
                elif result["guestscore"] < 2 and not bool(result["exception"]):
                    best_of_only_guest_losses += 1

    _stats = {
        "total": count_all_guest_scores + len(best_of_only_guest_ids),
        "wins": count_guest_wins + best_of_only_guest_wins,
        "losses": count_guest_losses + best_of_only_guest_losses,
        "win_ratio": round(
            100
            * (
                (count_guest_wins + best_of_only_guest_wins)
                / (count_all_guest_scores + len(best_of_only_guest_ids))
            ),
            5,
        ),
    }

    return _stats


def retrieve_bluff_stats_by_year(
    year: int,
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> dict[str, Any]:
    """Retrieves a dictionary containing Bluff the Listener statistics.

    Returned statistics includes a total count of shows with a unique
    Bluff the Listener segment, a count of times where the contestant
    chooses the correct story, and a count of times where the contestant
    does not choose the correct story.
    """
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT COUNT(s.showid)
        FROM ww_showbluffmap blm
        JOIN ww_shows s ON s.showid = blm.showid
        WHERE YEAR(s.showdate) = %s AND
        (s.bestof = 0 AND blm.chosenbluffpnlid IS NOT NULL AND
            blm.correctbluffpnlid IS NOT NULL) OR
        (s.bestof = 1 AND s.bestofuniquebluff = 1 AND
            blm.chosenbluffpnlid IS NOT NULL AND blm.correctbluffpnlid IS NOT
            NULL);
    """
    cursor = database_connection.cursor(dictionary=False)
    cursor.execute(query, (year,))
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return None

    count_unique_bluffs = result[0]

    query = """
        SELECT COUNT(s.showid)
        FROM ww_showbluffmap blm
        JOIN ww_shows s ON s.showid = blm.showid
        WHERE YEAR(s.showdate) = %s AND
        (s.bestof = 0 AND blm.chosenbluffpnlid = blm.correctbluffpnlid) OR
        (s.bestof = 1 AND s.bestofuniquebluff = 1 AND
            blm.chosenbluffpnlid = blm.correctbluffpnlid);
    """
    cursor = database_connection.cursor(dictionary=False)
    cursor.execute(query, (year,))
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return None

    count_chosen_correct = result[0]

    query = """
        SELECT COUNT(s.showid)
        FROM ww_showbluffmap blm
        JOIN ww_shows s ON s.showid = blm.showid
        WHERE YEAR(s.showdate) = %s AND
        (s.bestof = 0 AND blm.chosenbluffpnlid <> blm.correctbluffpnlid) OR
        (s.bestof = 1 AND s.bestofuniquebluff = 1 AND blm.chosenbluffpnlid
            <> blm.correctbluffpnlid);
    """
    cursor = database_connection.cursor(dictionary=False)
    cursor.execute(query, (year,))
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return None

    count_chosen_incorrect = result[0]

    return {
        "total": count_unique_bluffs,
        "correct": count_chosen_correct,
        "incorrect": count_chosen_incorrect,
        "correct_ratio": round(100 * (count_chosen_correct / count_unique_bluffs), 5),
    }


def retrieve_stats_all_years(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> dict[int, dict[str, Any]]:
    """Retrieves Not My Job and Bluff the Listener win stats for all years."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    _years_list = retrieve_all_years(database_connection=database_connection)

    if not _years_list:
        return None

    _years = {}
    for _year in _years_list:
        _years[_year] = {
            "not_my_job": retrieve_not_my_job_stats_by_year(
                year=_year, database_connection=database_connection
            ),
            "bluff": retrieve_bluff_stats_by_year(
                year=_year, database_connection=database_connection
            ),
        }

    return _years
