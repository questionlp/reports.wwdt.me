# -*- coding: utf-8 -*-
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Show Scoring Reports Functions"""
from collections import OrderedDict
from typing import List, Dict

import mysql.connector


def retrieve_show_details(
    show_id: int, database_connection: mysql.connector.connect
) -> Dict:
    """Retrieves host, scorekeeper, panelist, guest and location
    information for the requested show ID"""

    show_details = OrderedDict()

    # Retrieve host, scorekeeper and guest
    cursor = database_connection.cursor(dictionary=True)
    query = (
        "SELECT s.showdate, h.host, sk.scorekeeper, g.guest, "
        "gm.guestscore, gm.exception "
        "FROM ww_showhostmap hm "
        "JOIN ww_shows s ON s.showid = hm.showid "
        "JOIN ww_hosts h ON h.hostid = hm.hostid "
        "JOIN ww_showskmap skm ON skm.showid = hm.showid "
        "JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid "
        "JOIN ww_showguestmap gm ON gm.showid = hm.showid "
        "JOIN ww_guests g ON g.guestid = gm.guestid "
        "WHERE hm.showid = %s;"
    )
    cursor.execute(query, (show_id,))
    result = cursor.fetchone()

    if not result:
        return None

    show_details["date"] = result["showdate"].isoformat()
    show_details["host"] = result["host"]
    show_details["scorekeeper"] = result["scorekeeper"]
    guest = OrderedDict()
    guest["name"] = result["guest"]
    guest["score"] = result["guestscore"]
    guest["exception"] = bool(result["exception"])
    show_details["guest"] = guest

    # Retrieve show location details
    query = (
        "SELECT l.city, l.state, l.venue "
        "FROM ww_showlocationmap lm "
        "JOIN ww_locations l ON l.locationid = lm.locationid "
        "WHERE lm.showid = %s;"
    )
    cursor.execute(query, (show_id,))
    result = cursor.fetchone()

    if not result:
        show_details["location"] = None
    else:
        location = OrderedDict()
        location["city"] = result["city"]
        location["state"] = result["state"]
        location["venue"] = result["venue"]
        show_details["location"] = location

    # Retrieve panelists and their respective show rank and score
    query = (
        "SELECT p.panelist, pm.panelistscore "
        "FROM ww_showpnlmap pm "
        "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
        "WHERE pm.showid = %s "
        "ORDER BY pm.panelistscore DESC, pm.showpnlrank ASC;"
    )
    cursor.execute(query, (show_id,))
    result = cursor.fetchall()
    cursor.close()

    if not result:
        show_details["panelists"] = None
    else:
        panelists = []
        for row in result:
            panelist = OrderedDict()
            panelist["name"] = row["panelist"]
            panelist["score"] = row["panelistscore"]
            panelists.append(panelist)

        show_details["panelists"] = panelists

    return show_details


def retrieve_shows_all_high_scoring(
    database_connection: mysql.connector.connect,
) -> List[Dict]:
    """Retrieves details from shows with a panelist total score greater
    than or equal to 50"""
    cursor = database_connection.cursor(dictionary=True)
    query = (
        "SELECT s.showid, s.showdate, SUM(pm.panelistscore) AS total "
        "FROM ww_showpnlmap pm "
        "JOIN ww_shows s ON s.showid = pm.showid "
        "WHERE s.bestof = 0 AND s.repeatshowid IS NULL "
        "GROUP BY s.showdate "
        "HAVING SUM(pm.panelistscore) >= 50 "
        "ORDER BY SUM(pm.panelistscore) DESC, s.showdate DESC;"
    )
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    shows = []
    for row in result:
        show_id = row["showid"]
        show_details = retrieve_show_details(show_id, database_connection)
        show_details["total_score"] = row["total"]
        if show_details:
            shows.append(show_details)

    return shows


def retrieve_shows_all_low_scoring(
    database_connection: mysql.connector.connect,
) -> List[Dict]:
    """Retrieves details from shows with a panelist total score less
    than 30. Excludes the 20th anniversary show due to unique Lightning
    Fill-in-the-Blank segment."""
    cursor = database_connection.cursor(dictionary=True)
    query = (
        "SELECT s.showid, s.showdate, SUM(pm.panelistscore) AS total "
        "FROM ww_showpnlmap pm "
        "JOIN ww_shows s ON s.showid = pm.showid "
        "WHERE s.bestof = 0 AND s.repeatshowid IS NULL "
        "AND s.showdate <> '2018-10-27' "
        "GROUP BY s.showdate "
        "HAVING SUM(pm.panelistscore) < 30 "
        "ORDER BY SUM(pm.panelistscore) ASC, s.showdate DESC;"
    )
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    shows = []
    for row in result:
        show_id = row["showid"]
        show_details = retrieve_show_details(show_id, database_connection)
        show_details["total_score"] = row["total"]
        if show_details:
            shows.append(show_details)

    return shows


def retrieve_shows_panelist_score_sum_match(
    database_connection: mysql.connector.connect,
) -> List[Dict]:
    """Retrieves shows in which the score of panelist in first place
    matches the sum of the scores for the other two panelists. Excludes
    the 20th anniversary show due to unique Lightning Fill-in-the-Blank
    segment."""
    cursor = database_connection.cursor(dictionary=True)
    query = (
        "SELECT s.showdate, pm.panelistid, p.panelist, p.panelistslug, "
        "pm.panelistscore, pm.showpnlrank "
        "FROM ww_showpnlmap pm "
        "JOIN ww_shows s ON s.showid = pm.showid "
        "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
        "WHERE s.bestof = 0 AND s.repeatshowid IS NULL AND "
        "s.showdate <> '2018-10-27' AND "
        "pm.panelistscore IS NOT NULL "
        "ORDER BY s.showdate ASC, pm.panelistscore DESC;"
    )
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    shows = OrderedDict()
    for row in result:
        show_date = row["showdate"].isoformat()
        if show_date not in shows:
            shows[show_date] = []

        score = OrderedDict()
        score["panelist_id"] = row["panelistid"]
        score["panelist"] = row["panelist"]
        score["panelist_slug"] = row["panelistslug"]
        score["score"] = row["panelistscore"]
        score["rank"] = row["showpnlrank"]
        shows[show_date].append(score)

    shows_match = OrderedDict()
    for show in shows:
        show_info = shows[show]
        score_1 = show_info[0]["score"]
        score_2 = show_info[1]["score"]
        score_3 = show_info[2]["score"]
        if score_1 == score_2 + score_3:
            shows_match[show] = show_info

    return shows_match
