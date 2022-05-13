# -*- coding: utf-8 -*-
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Panel Gender Mix Report Functions"""

from collections import OrderedDict
from typing import Dict, List, Text
import mysql.connector
import numpy

def retrieve_show_years(database_connection: mysql.connector.connect
                       ) -> List[int]:
    """Retrieve a list of available show years"""
    cursor = database_connection.cursor()
    query = ("SELECT DISTINCT YEAR(showdate) "
             "FROM ww_shows "
             "ORDER BY YEAR(showdate) ASC;")
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    years = []
    for row in result:
        years.append(row[0])

    return years

def retrieve_scores_by_year_gender(year: int,
                                   gender: Text,
                                   database_connection: mysql.connector.connect
                                  ) -> List[int]:
    """Retrieve a list of panelist scores for a given year and
    panelists of the requested gender"""

    if not gender:
        return None

    panelist_gender = gender[0].upper()

    cursor = database_connection.cursor(dictionary=True)
    query = ("SELECT pm.panelistscore FROM ww_showpnlmap pm "
             "JOIN ww_shows s ON s.showid = pm.showid "
             "JOIN ww_panelists p ON p.panelistid = pm.panelistid "
             "WHERE s.bestof = 0 AND s.repeatshowid IS NULL "
             "AND pm.panelistscore IS NOT NULL "
             "AND p.panelistgender = %s "
             "AND YEAR(s.showdate) = %s "
             "ORDER BY s.showdate ASC;")
    cursor.execute(query, (panelist_gender, year))
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    scores = []
    for row in result:
        scores.append(row["panelistscore"])

    return scores

def retrieve_stats_by_year_gender(database_connection: mysql.connector.connect
                                  ) -> Dict:
    """Retrieve statistics about panelist scores broken out by year
    and gender"""

    show_years = retrieve_show_years(database_connection)

    all_stats = OrderedDict()
    for year in show_years:
        all_stats[year] = OrderedDict()
        for gender in ["F", "M"]:
            stats = OrderedDict()
            scores = retrieve_scores_by_year_gender(year=year,
                                                    gender=gender,
                                                    database_connection=database_connection)
            if scores:
                stats["minimum"] = int(numpy.amin(scores))
                stats["maximum"] = int(numpy.amax(scores))
                stats["mean"] = round(numpy.mean(scores), 4)
                stats["median"] = int(numpy.median(scores))
                stats["standard_deviation"] = round(numpy.std(scores), 4)
                stats["count"] = len(scores)
                stats["total"] = int(numpy.sum(scores))
                all_stats[year][gender] = stats
            else:
                all_stats[year][gender] = None

    return all_stats
