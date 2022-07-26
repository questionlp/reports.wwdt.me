# -*- coding: utf-8 -*-
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM All Women Panel Report Functions"""
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


def retrieve_shows_all_women_panel(
    database_connection: mysql.connector.connect,
) -> List[Dict]:
    """Retrieves details from all shows that have had an all women
    panel"""
    cursor = database_connection.cursor(dictionary=True)
    query = (
        "SELECT pm.showid "
        "FROM ww_showpnlmap pm "
        "JOIN ww_shows s ON s.showid = pm.showid "
        "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
        "WHERE s.bestof = 0 AND s.repeatshowid IS NULL "
        "AND s.showdate <> '2018-10-27' "
        "AND p.panelistgender = 'F' "
        "GROUP BY pm.showid "
        "HAVING COUNT(s.showid) = 3;"
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
        if show_details:
            shows.append(show_details)

    return shows
