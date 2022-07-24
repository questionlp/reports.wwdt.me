# -*- coding: utf-8 -*-
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Scorekeeper Introductions Report Functions"""
from collections import OrderedDict
from typing import List, Dict

import mysql.connector


def retrieve_scorekeepers_with_introductions(
    database_connection: mysql.connector.connect,
) -> List[Dict]:
    """Retrieve a list of scorekeepers that have show introduction entries
    in the database"""

    scorekeepers = []
    cursor = database_connection.cursor(dictionary=True)
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

    for row in result:
        scorekeeper_info = OrderedDict()
        scorekeeper_info["id"] = row["scorekeeperid"]
        scorekeeper_info["name"] = row["scorekeeper"]
        scorekeeper_info["slug"] = row["scorekeeperslug"]
        scorekeepers.append(scorekeeper_info)

    return scorekeepers


def retrieve_all_scorekeeper_introductions(
    database_connection: mysql.connector.connect,
) -> Dict:
    """Retrieve all scorekeeper introductions from the database"""

    scorekeepers = retrieve_scorekeepers_with_introductions(database_connection)
    all_introductions = OrderedDict()

    cursor = database_connection.cursor(dictionary=True)
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
                show_info = OrderedDict()
                show_info["id"] = row["showid"]
                show_info["date"] = row["showdate"].isoformat()
                show_info["best_of"] = bool(row["bestof"])
                show_info["repeat_show"] = bool(row["repeatshowid"])
                show_info["introduction"] = row["description"]
                scorekeeper_intros.append(show_info)

        all_introductions[scorekeeper["id"]] = scorekeeper_intros

    cursor.close()
    return all_introductions
