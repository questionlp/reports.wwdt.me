# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Show Panel Gender Mix Report Functions"""
from typing import Any, Dict, List

import mysql.connector


def retrieve_show_years(database_connection: mysql.connector.connect) -> List[int]:
    """Retrieve a list of show years available in the database"""

    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT DISTINCT YEAR(s.showdate) AS year FROM ww_shows s "
        "ORDER BY YEAR(s.showdate) ASC;"
    )
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    return [row.year for row in result]


def retrieve_panel_gender_count_by_year(
    year: int, gender: str, database_connection: mysql.connector.connect
) -> int:
    """Get a count of shows for the requested year that has the
    requested number of panelists of a given gender"""

    # panelistgender field only contains a single letter
    gender_tag = gender[0].upper()

    if not database_connection.is_connected():
        database_connection.reconnect()

    counts = {}
    for gender_count in range(0, 4):
        cursor = database_connection.cursor(dictionary=False)
        query = (
            "SELECT s.showdate FROM ww_showpnlmap pm "
            "JOIN ww_shows s ON s.showid = pm.showid "
            "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
            "WHERE s.bestof = 0 AND s.repeatshowid IS NULL "
            "AND p.panelistgender = %s "
            "AND year(s.showdate) = %s "
            "AND s.showdate <> '2018-10-27' "  # Exclude 25th anniversary special
            "GROUP BY s.showdate "
            "HAVING COUNT(p.panelistgender) = %s;"
        )
        cursor.execute(
            query,
            (
                gender_tag,
                year,
                gender_count,
            ),
        )
        cursor.fetchall()
        counts["{}{}".format(gender_count, gender_tag)] = cursor.rowcount
        cursor.close()

    counts["total"] = sum(counts.values())
    return counts


def panel_gender_mix_breakdown(
    gender: str, database_connection: mysql.connector.connect
) -> Dict[str, Any]:
    """Calculate the panel gender breakdown for all show years and
    return a dictionary containing count for each year"""

    if not database_connection.is_connected():
        database_connection.reconnect()

    show_years = retrieve_show_years(database_connection=database_connection)

    gender_mix_breakdown = {}
    for year in show_years:
        count = retrieve_panel_gender_count_by_year(
            year=year, gender=gender, database_connection=database_connection
        )
        gender_mix_breakdown[year] = count

    return gender_mix_breakdown
