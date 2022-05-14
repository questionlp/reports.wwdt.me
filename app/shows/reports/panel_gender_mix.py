# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Panel Gender Mix Report Functions"""
from typing import Any, Dict, List

from flask import current_app
import mysql.connector


def retrieve_show_years() -> List[int]:
    """Retrieve a list of show years available in the database"""

    database_connection = mysql.connector.connect(**current_app.config["database"])
    cursor = database_connection.cursor()
    query = (
        "SELECT DISTINCT YEAR(s.showdate) FROM ww_shows s "
        "ORDER BY YEAR(s.showdate) ASC;"
    )
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    database_connection.close()

    if not result:
        return None

    years = []
    for row in result:
        years.append(row[0])

    return years


def retrieve_panel_gender_count_by_year(year: int, gender: str) -> int:
    """Get a count of shows for the requested year that has the
    requested number of panelists of a given gender"""

    # panelistgender field only contains a single letter
    gender_tag = gender[0].upper()

    database_connection = mysql.connector.connect(**current_app.config["database"])
    cursor = database_connection.cursor()

    counts = {}
    for gender_count in range(0, 4):
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
    database_connection.close()

    total = sum(counts.values())
    counts["total"] = total
    return counts


def panel_gender_mix_breakdown(gender: str) -> Dict[str, Any]:
    """Calculate the panel gender breakdown for all show years and
    return an OrderedDict containing count for each year"""

    show_years = retrieve_show_years()

    gender_mix_breakdown = {}
    for year in show_years:
        count = retrieve_panel_gender_count_by_year(year=year, gender=gender)
        gender_mix_breakdown[year] = count

    return gender_mix_breakdown
