# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Guest Scores Report Functions"""

from typing import Any, Dict, List

from flask import current_app
import mysql.connector


def retrieve_scoring_exceptions(
    guest_id: int,
) -> List[Dict[str, Any]]:
    """Retrieve a list of instances where a requested Not My Job guest
    has had a scoring exception"""

    database_connection = mysql.connector.connect(**current_app.config["database"])
    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT g.guestid, g.guest, s.showid, s.showdate, "
        "gm.guestscore, gm.exception, sn.shownotes "
        "FROM ww_showguestmap gm "
        "JOIN ww_shows s ON s.showid = gm.showid "
        "JOIN ww_guests g ON g.guestid = gm.guestid "
        "JOIN ww_shownotes sn on sn.showid = gm.showid "
        "WHERE g.guestid = %s "
        "AND s.bestof = 0 AND s.repeatshowid IS NULL "
        "AND gm.exception = 1 "
        "ORDER BY s.showdate ASC;"
    )
    cursor.execute(query, (guest_id,))
    result = cursor.fetchall()
    cursor.close()
    database_connection.close()

    if not result:
        return None

    _exceptions = []
    for row in result:
        show = {}
        show["id"] = row.showid
        show["date"] = row.showdate.isoformat()
        show["score"] = row.guestscore
        show["exception"] = bool(row.exception)
        show["notes"] = row.shownotes
        _exceptions.append(show)

    return _exceptions


def retrieve_guest_scores(
    guest_id: int,
) -> List[Dict[str, Any]]:
    """Retrieve a list of instances where a requested Not My Job guest
    has received three points"""

    database_connection = mysql.connector.connect(**current_app.config["database"])
    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT g.guestid, g.guest, s.showid, s.showdate, "
        "gm.guestscore, gm.exception, sn.shownotes "
        "FROM ww_showguestmap gm "
        "JOIN ww_shows s ON s.showid = gm.showid "
        "JOIN ww_guests g ON g.guestid = gm.guestid "
        "JOIN ww_shownotes sn on sn.showid = gm.showid "
        "WHERE g.guestid = %s "
        "AND s.bestof = 0 AND s.repeatshowid IS NULL "
        "AND gm.exception = 1 "
        "ORDER BY s.showdate ASC;"
    )
    cursor.execute(query, (guest_id,))
    result = cursor.fetchall()
    cursor.close()
    database_connection.close()

    if not result:
        return None

    _scores = []
    for row in result:
        show = {}
        show["id"] = row.showid
        show["date"] = row.showdate.isoformat()
        show["score"] = row.guestscore
        show["exception"] = bool(row.exception)
        show["notes"] = row.shownotes
        _scores.append(show)

    return _scores


def retrieve_all_scoring_exceptions() -> List[Dict[str, Any]]:
    """Retrieve a list of all Not My Job scoring exceptions"""

    database_connection = mysql.connector.connect(**current_app.config["database"])
    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT DISTINCT g.guestid, g.guest, g.guestslug "
        "FROM ww_showguestmap gm "
        "JOIN ww_shows s ON s.showid = gm.showid "
        "JOIN ww_guests g ON g.guestid = gm.guestid "
        "WHERE s.bestof = 0 AND s.repeatshowid IS NULL "
        "AND gm.exception = 1 "
        "ORDER BY g.guest ASC;"
    )
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    database_connection.close()

    if not result:
        return None

    _exceptions = []
    for row in result:
        guest = {}
        guest["id"] = row.guestid
        guest["name"] = row.guest
        guest["slug"] = row.guestslug
        guest["exceptions"] = retrieve_scoring_exceptions(guest_id=row.guestid)
        _exceptions.append(guest)

    return _exceptions


def retrieve_all_three_pointers() -> List[Dict]:
    """Retrieve a list instances where Not My Job guests have answered
    all three questions correctly or received all three points"""

    database_connection = mysql.connector.connect(**current_app.config["database"])
    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "(SELECT g.guestid, g.guest, g.guestslug, s.showid, s.showdate, "
        " gm.guestscore, gm.exception, sk.scorekeeperid, sk.scorekeeper, "
        " sk.scorekeeperslug, sn.shownotes "
        " FROM ww_showguestmap gm "
        " JOIN ww_shows s ON s.showid = gm.showid "
        " JOIN ww_guests g ON g.guestid = gm.guestid "
        " JOIN ww_shownotes sn ON sn.showid = gm.showid "
        " JOIN ww_showskmap skm ON skm.showid = gm.showid "
        " JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid "
        " WHERE s.bestof = 0 AND s.repeatshowid IS NULL "
        " AND gm.guestscore = 3 "
        ") "
        "UNION "
        "(SELECT g.guestid, g.guest, g.guestslug, s.showid, s.showdate, "
        " gm.guestscore, gm.exception, sk.scorekeeperid, sk.scorekeeper, "
        " sk.scorekeeperslug, sn.shownotes "
        " FROM ww_showguestmap gm "
        " JOIN ww_shows s ON s.showid = gm.showid "
        " JOIN ww_guests g ON g.guestid = gm.guestid "
        " JOIN ww_shownotes sn ON sn.showid = gm.showid "
        " JOIN ww_showskmap skm ON skm.showid = gm.showid "
        " JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid "
        " WHERE s.bestof = 1 AND s.repeatshowid IS NULL "
        " AND gm.guestscore = 3 "
        " AND g.guestid NOT IN ( "
        " SELECT gm.guestid "
        " FROM ww_showguestmap gm "
        " JOIN ww_shows s ON s.showid = gm.showid "
        " WHERE s.bestof = 0 AND s.repeatshowid IS NULL "
        " ) "
        ")"
        "ORDER BY guest ASC, showdate ASC;"
    )
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    database_connection.close()

    if not result:
        return None

    three_pointers = []
    for row in result:
        guest = {}
        guest["id"] = row.guestid
        guest["name"] = row.guest
        guest["slug"] = row.guestslug
        guest["show_date"] = row.showdate.isoformat()
        guest["show_scorekeeper"] = row.scorekeeper
        guest["show_scorekeeper_slug"] = row.scorekeeperslug
        guest["score"] = row.guestscore
        guest["exception"] = bool(row.exception)
        guest["show_notes"] = row.shownotes
        three_pointers.append(guest)

    return three_pointers
