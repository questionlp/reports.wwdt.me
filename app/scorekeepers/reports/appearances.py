# -*- coding: utf-8 -*-
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Scorekeeper Appearances Report Functions"""
from collections import OrderedDict
from typing import Dict, List, Text

import mysql.connector


def retrieve_all_scorekeepers(
    database_connection: mysql.connector.connect,
) -> List[Dict]:
    """Retrieves a dictionary for all available scorekeepers from the
    database"""

    cursor = database_connection.cursor(dictionary=True)
    query = (
        "SELECT sk.scorekeeperid, sk.scorekeeper, sk.scorekeeperslug "
        "FROM ww_scorekeepers sk "
        "WHERE sk.scorekeeper <> '(TBD)' "
        "ORDER BY sk.scorekeeperslug ASC;"
    )
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    scorekeepers = []
    for row in result:
        scorekeeper = OrderedDict()
        scorekeeper["name"] = row["scorekeeper"]
        scorekeeper["slug"] = row["scorekeeperslug"]
        scorekeepers.append(scorekeeper)

    return scorekeepers


def retrieve_appearances_by_scorekeeper(
    scorekeeper_slug: Text, database_connection: mysql.connector.connect
) -> Dict:
    """Retrieve appearance data for the requested scorekeeper"""

    cursor = database_connection.cursor(dictionary=True)
    query = (
        "SELECT ( "
        "SELECT COUNT(skm.showid) FROM ww_showskmap skm "
        "JOIN ww_shows s ON s.showid = skm.showid "
        "JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid "
        "WHERE s.bestof = 0 AND s.repeatshowid IS NULL AND "
        "sk.scorekeeperslug = %s ) AS regular, ( "
        "SELECT COUNT(skm.showid) FROM ww_showskmap skm "
        "JOIN ww_shows s ON s.showid = skm.showid "
        "JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid "
        "WHERE sk.scorekeeperslug = %s ) AS allshows;"
    )
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
        return None

    appearances = OrderedDict()
    appearances["regular"] = result["regular"]
    appearances["all"] = result["allshows"]

    return appearances


def retrieve_first_most_recent_appearances(
    scorekeeper_slug: Text, database_connection: mysql.connector.connect
) -> Dict:
    """Retrieve first and most recent appearances for both regular
    and all shows for the requested scorekeeper"""

    cursor = database_connection.cursor(dictionary=True)
    query = (
        "SELECT MIN(s.showdate) AS min, MAX(s.showdate) AS max "
        "FROM ww_showskmap skm "
        "JOIN ww_shows s ON s.showid = skm.showid "
        "JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid "
        "WHERE sk.scorekeeperslug = %s "
        "AND s.bestof = 0 "
        "AND s.repeatshowid IS null;"
    )
    cursor.execute(query, (scorekeeper_slug,))
    result = cursor.fetchone()

    if not result:
        return None

    appearance_info = OrderedDict()
    appearance_info["first"] = result["min"].isoformat()
    appearance_info["most_recent"] = result["max"].isoformat()

    query = (
        "SELECT MIN(s.showdate) AS min, MAX(s.showdate) AS max "
        "FROM ww_showskmap skm "
        "JOIN ww_shows s ON s.showid = skm.showid "
        "JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid "
        "WHERE sk.scorekeeperslug = %s;"
    )
    cursor.execute(query, (scorekeeper_slug,))
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return appearance_info

    appearance_info["first_all"] = result["min"].isoformat()
    appearance_info["most_recent_all"] = result["max"].isoformat()

    return appearance_info


def retrieve_appearance_summaries(
    database_connection: mysql.connector.connection,
) -> List[Dict]:
    """Retrieve scorekeeper appearance summary, including appearance
    counts, and first and most recent appearances"""
    scorekeepers = retrieve_all_scorekeepers(database_connection)

    if not scorekeepers:
        return None

    scorekeepers_summary = OrderedDict()
    for scorekeeper in scorekeepers:
        appearance_count = retrieve_appearances_by_scorekeeper(
            scorekeeper["slug"], database_connection
        )
        first_most_recent = retrieve_first_most_recent_appearances(
            scorekeeper["slug"], database_connection
        )
        info = OrderedDict()
        info["slug"] = scorekeeper["slug"]
        info["name"] = scorekeeper["name"]
        info["regular_shows"] = appearance_count["regular"]
        info["all_shows"] = appearance_count["all"]
        info["first"] = first_most_recent["first"]
        info["first_all"] = first_most_recent["first_all"]
        info["most_recent"] = first_most_recent["most_recent"]
        info["most_recent_all"] = first_most_recent["most_recent_all"]
        scorekeepers_summary[scorekeeper["slug"]] = info

    return scorekeepers_summary
