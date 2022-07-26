# -*- coding: utf-8 -*-
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Show Counts Report Functions"""
from collections import OrderedDict
from typing import List, Dict

import mysql.connector


def retrieve_show_counts_by_year(
    database_connection: mysql.connector.connect,
) -> Dict[int, int]:
    """Retrieve the number of Regular, Best Of, Repeat and Repeat/Best
    Of shows broken down by year"""

    years = []
    cursor = database_connection.cursor(dictionary=True)
    query = (
        "SELECT DISTINCT YEAR(showdate) AS 'year' FROM ww_shows "
        "ORDER BY showdate ASC;"
    )
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    for row in result:
        years.append(int(row["year"]))

    show_counts = OrderedDict()
    for year in years:
        cursor = database_connection.cursor(dictionary=True)
        query = (
            "SELECT "
            "(SELECT COUNT(showid) FROM ww_shows "
            " WHERE YEAR(showdate) = %s AND showdate <= NOW() "
            " AND bestof = 0 AND repeatshowid IS NULL) AS 'regular', "
            "(SELECT COUNT(showid) FROM ww_shows "
            " WHERE YEAR(showdate) = %s AND showdate <= NOW() "
            " AND bestof = 1 AND repeatshowid IS NULL) AS 'bestof', "
            "(SELECT COUNT(showid) FROM ww_shows "
            " WHERE YEAR(showdate) = %s AND showdate <= NOW() "
            " AND bestof = 0 AND repeatshowid IS NOT NULL) AS 'repeat', "
            "(SELECT COUNT(showid) FROM ww_shows "
            " WHERE YEAR(showdate) = %s AND showdate <= NOW() "
            " AND bestof = 1 AND repeatshowid IS NOT NULL) AS 'repeat_bestof';"
        )
        cursor.execute(
            query,
            (
                year,
                year,
                year,
                year,
            ),
        )
        result = cursor.fetchone()
        cursor.close()

        if not result:
            show_counts[year] = None
        else:
            counts = OrderedDict()
            counts["regular"] = result["regular"]
            counts["best_of"] = result["bestof"]
            counts["repeat"] = result["repeat"]
            counts["repeat_best_of"] = result["repeat_bestof"]
            counts["total"] = (
                result["regular"]
                + result["bestof"]
                + result["repeat"]
                + result["repeat_bestof"]
            )
            show_counts[year] = counts

    return show_counts
