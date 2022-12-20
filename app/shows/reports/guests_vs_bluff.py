# -*- coding: utf-8 -*-
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Show Not My Job Guest Wins Rate vs Bluff the Listener Wins Rate
Report Functions"""
from typing import Any, Dict

import mysql.connector

from app.guests.reports.best_of_only import retrieve_best_of_only_guests


def retrieve_not_my_job_stats(
    database_connection: mysql.connector.connect,
) -> Dict[str, Any]:
    """Returns a dictionary containing the total number of Not My Job
    guest entries that have a score entered, total number of times a
    Not My Job guest has won (including exceptions), and a total number
    of times a Not My Job guest has lost."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    # Get a count of all Not My Job guest entries with scores and are
    # from shows that are not Best Of or repeats
    cursor = database_connection.cursor(dictionary=False)
    query = (
        "SELECT COUNT(g.guestid) "
        "FROM ww_showguestmap gm "
        "JOIN ww_guests g ON g.guestid = gm.guestid "
        "JOIN ww_shows s ON  s.showid = gm.showid "
        "WHERE s.bestof = 0 AND s.repeatshowid IS NULL "
        "AND g.guestslug <> 'none' "
        "AND gm.guestscore IS NOT NULL;"
    )
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return None

    count_all_guest_scores = result[0]

    # Get a count of all Not My Job guest entries in which a guest won
    # outright or was given a win via a scoring exception
    cursor = database_connection.cursor(dictionary=False)
    query = (
        "SELECT COUNT(g.guestid) "
        "FROM ww_showguestmap gm "
        "JOIN ww_guests g ON g.guestid = gm.guestid "
        "JOIN ww_shows s ON s.showid = gm.showid "
        "WHERE s.bestof = 0 AND s.repeatshowid IS NULL "
        "AND g.guestslug = 'none' "
        "AND (gm.guestscore >= 2 OR gm.exception = 1);"
    )
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return None

    count_guest_wins = result[0]

    # Get a count of all Not My Job guest entries in which a guest did
    # not win
    cursor = database_connection.cursor(dictionary=False)
    query = (
        "SELECT COUNT(g.guestid) "
        "FROM ww_showguestmap gm "
        "JOIN ww_guests g ON g.guestid = gm.guestid "
        "JOIN ww_shows s ON s.showid = gm.showid "
        "WHERE s.bestof = 0 AND s.repeatshowid IS NULL "
        "AND g.guestslug = 'none' "
        "AND (gm.guestscore < 2 AND gm.exception = 0);"
    )
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return None

    count_guest_losses = result[0]

    # Get a list of Not My Job guests that have only appeared on Best Of
    # shows
    cursor = database_connection.cursor(dictionary=False)
    query = (
        "SELECT DISTINCT g.guestid "
        "FROM ww_showguestmap gm "
        "JOIN ww_shows s ON s.showid = gm.showid "
        "JOIN ww_guests g ON g.guestid = gm.guestid "
        "WHERE s.bestof = 1 AND s.repeatshowid IS NULL "
        "AND g.guestid NOT IN ( "
        "SELECT gm.guestid "
        "FROM ww_showguestmap gm "
        "JOIN ww_shows s ON s.showid = gm.showid "
        "WHERE s.bestof = 0 AND s.repeatshowid IS NULL );"
    )
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    best_of_only_guest_ids = [guest[0] for guest in result]
    best_of_only_guest_wins = 0
    best_of_only_guest_losses = 0

    for guest_id in best_of_only_guest_ids:
        cursor = database_connection.cursor(named_tuple=True)
        query = (
            "SELECT s.showdate, gm.guestscore, gm.exception "
            "FROM ww_showguestmap gm "
            "JOIN ww_shows s ON s.showid = gm.showid "
            "WHERE s.repeatshowid IS NULL "
            "AND gm.guestid = %s "
            "ORDER BY s.showdate ASC "
            "LIMIT 1;"
        )
        cursor.execute(query, (guest_id,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            if result.guestscore >= 2 or bool(result.exception):
                best_of_only_guest_wins += 1
            elif result.guestscore < 2 and not bool(result.exception):
                best_of_only_guest_losses += 1

    return {
        "total": count_all_guest_scores + len(best_of_only_guest_ids),
        "wins": count_guest_wins + best_of_only_guest_wins,
        "losses": count_guest_losses + best_of_only_guest_losses,
    }


def retrieve_bluff_stats(
    database_connection: mysql.connector.connect,
) -> Dict[str, Any]:
    """Retrieves a dictionary containing statistics for the Bluff the
    Listener segment with a total count of shows with a unique Bluff
    the Listener segment, a count of times where the contestant chooses
    the correct story, and a count of times where the contestant
    does not choose the correct story."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(dictionary=False)
    query = (
        "SELECT COUNT(s.showid) "
        "FROM ww_showbluffmap blm "
        "JOIN ww_shows s ON s.showid = blm.showid "
        "WHERE "
        "(s.bestof = 0 AND blm.chosenbluffpnlid IS NOT NULL AND "
        " blm.correctbluffpnlid IS NOT NULL) OR "
        "(s.bestof = 1 AND s.bestofuniquebluff = 1 AND "
        " blm.chosenbluffpnlid IS NOT NULL AND blm.correctbluffpnlid IS NOT "
        " NULL);"
    )
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return None

    count_unique_bluffs = result[0]

    cursor = database_connection.cursor(dictionary=False)
    query = (
        "SELECT COUNT(s.showid) "
        "FROM ww_showbluffmap blm "
        "JOIN ww_shows s ON s.showid = blm.showid "
        "WHERE "
        "(s.bestof = 0 AND blm.chosenbluffpnlid = blm.correctbluffpnlid) OR "
        "(s.bestof = 1 AND s.bestofuniquebluff = 1 AND "
        " blm.chosenbluffpnlid = blm.correctbluffpnlid);"
    )
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return None

    count_chosen_correct = result[0]

    cursor = database_connection.cursor(dictionary=False)
    query = (
        "SELECT COUNT(s.showid) "
        "FROM ww_showbluffmap blm "
        "JOIN ww_shows s ON s.showid = blm.showid "
        "WHERE "
        "(s.bestof = 0 AND blm.chosenbluffpnlid <> blm.correctbluffpnlid) OR "
        "(s.bestof = 1 AND s.bestofuniquebluff = 1 AND blm.chosenbluffpnlid "
        " <> blm.correctbluffpnlid);"
    )
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return None

    count_chosen_incorrect = result[0]

    return {
        "total": count_unique_bluffs,
        "correct": count_chosen_correct,
        "incorrect": count_chosen_incorrect,
    }
