# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Panel Gender Mix Report Functions"""
from typing import Any, Dict, List

import mysql.connector
import numpy


def retrieve_show_years(database_connection: mysql.connector.connect) -> List[int]:
    """Retrieve a list of available show years"""

    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor()
    query = (
        "SELECT DISTINCT YEAR(showdate) "
        "FROM ww_shows "
        "ORDER BY YEAR(showdate) ASC;"
    )
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    return [row[0] for row in result]


def retrieve_scores_by_year_gender(
    year: int, gender: str, database_connection: mysql.connector.connect
) -> List[int]:
    """Retrieve a list of panelist scores for a given year and
    panelists of the requested gender"""

    if not gender:
        return None

    panelist_gender = gender[0].upper()

    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT pm.panelistscore FROM ww_showpnlmap pm "
        "JOIN ww_shows s ON s.showid = pm.showid "
        "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
        "WHERE s.bestof = 0 AND s.repeatshowid IS NULL "
        "AND pm.panelistscore IS NOT NULL "
        "AND p.panelistgender = %s "
        "AND YEAR(s.showdate) = %s "
        "ORDER BY s.showdate ASC;"
    )
    cursor.execute(query, (panelist_gender, year))
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    return [row.panelistscore for row in result]


def retrieve_stats_by_year_gender(
    database_connection: mysql.connector.connect,
) -> Dict[str, Any]:
    """Retrieve statistics about panelist scores broken out by year
    and gender"""

    show_years = retrieve_show_years(database_connection)

    all_stats = {}
    for year in show_years:
        all_stats[year] = {}
        for gender in ["F", "M"]:
            scores = retrieve_scores_by_year_gender(
                year=year, gender=gender, database_connection=database_connection
            )
            if scores:
                all_stats[year][gender] = {
                    "minimum": int(numpy.amin(scores)),
                    "maximum": int(numpy.amax(scores)),
                    "mean": round(numpy.mean(scores), 4),
                    "median": int(numpy.median(scores)),
                    "standard_deviation": round(numpy.std(scores), 4),
                    "count": len(scores),
                    "total": int(numpy.sum(scores)),
                }
            else:
                all_stats[year][gender] = None

    return all_stats
