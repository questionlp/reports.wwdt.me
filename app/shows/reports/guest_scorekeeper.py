# -*- coding: utf-8 -*-
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Show Guest Scorekeeper Report Functions"""
from collections import OrderedDict
from typing import List, Dict

import mysql.connector

from app.shows.reports import show_details


def retrieve_shows_guest_scorekeeper(
    database_connection: mysql.connector.connect,
) -> List[Dict]:
    """Retrieve a list of shows with guest scorekeepers"""
    shows = []
    cursor = database_connection.cursor(dictionary=True)
    query = (
        "SELECT s.showid, s.showdate, s.bestof, s.repeatshowid, h.host, "
        "h.hostslug, hm.guest AS host_guest, sk.scorekeeper, "
        "sk.scorekeeperslug, l.venue, l.city, l.state "
        "FROM ww_showhostmap hm "
        "JOIN ww_hosts h ON h.hostid = hm.hostid "
        "JOIN ww_showskmap skm ON skm.showid = hm.showid "
        "JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid "
        "JOIN ww_shows s ON s.showid = hm.showid "
        "JOIN ww_showlocationmap lm ON lm.showid = hm.showid "
        "JOIN ww_locations l ON l.locationid = lm.locationid "
        "WHERE skm.guest = 1 "
        "ORDER BY s.showdate ASC "
    )
    cursor.execute(query)
    result = cursor.fetchall()

    if not result:
        return None

    for row in result:
        show = OrderedDict()
        show_id = row["showid"]
        show["date"] = row["showdate"].isoformat()
        show["best_of"] = bool(row["bestof"])
        show["repeat"] = bool(row["repeatshowid"])
        show["location"] = OrderedDict()
        show["location"]["venue"] = row["venue"]
        show["location"]["city"] = row["city"]
        show["location"]["state"] = row["state"]
        show["host"] = row["host"]
        show["host_slug"] = row["hostslug"]
        show["host_guest"] = bool(row["host_guest"])
        show["scorekeeper"] = row["scorekeeper"]
        show["scorekeeper_slug"] = row["scorekeeperslug"]
        show["panelists"] = show_details.retrieve_show_panelists(
            show_id, database_connection
        )
        show["guests"] = show_details.retrieve_show_guests(show_id, database_connection)
        shows.append(show)

    return shows
