# -*- coding: utf-8 -*-
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Show Counts Report Functions"""
from typing import Dict

import mysql.connector


def retrieve_show_counts_by_year(
    database_connection: mysql.connector.connect,
) -> Dict[int, int]:
    """Retrieve the number of Regular, Best Of, Repeat and Repeat/Best
    Of shows broken down by year"""

    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT DISTINCT YEAR(showdate) AS 'year' FROM ww_shows "
        "ORDER BY showdate ASC;"
    )
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    years = []
    for row in result:
        years.append(int(row.year))

    show_counts = {}
    for year in years:
        cursor = database_connection.cursor(named_tuple=True)
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
            show_counts[year] = {
                "regular": result.regular,
                "best_of": result.bestof,
                "repeat": result.repeat,
                "repeat_best_of": result.repeat_bestof,
                "total": (
                    result.regular
                    + result.bestof
                    + result.repeat
                    + result.repeat_bestof
                ),
            }

    return show_counts
