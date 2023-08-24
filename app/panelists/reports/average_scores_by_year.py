# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2023 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Panelists Average Scores Report Functions"""
from decimal import Decimal
from re import U
from typing import List, Dict, Union

from flask import current_app
import mysql.connector


def empty_years_average(database_connection: mysql.connector.connect) -> Dict[int, int]:
    """Retrieve a dictionary containing a list of available years as
    keys and zeroes for values"""
    if not database_connection.is_connected():
        database_connection.reconnect()

    # Retrieve available show years
    cursor = database_connection.cursor(named_tuple=True)
    query = """
        SELECT DISTINCT YEAR(showdate) AS year
        FROM ww_shows
        ORDER BY YEAR(showdate) ASC;
        """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    return {row.year: 0 for row in result}


def retrieve_panelist_yearly_average(
    panelist_slug: str,
    database_connection: mysql.connector.connect,
    use_decimal_scores: bool = False,
) -> Dict[str, Union[str, List[Union[float, Decimal]]]]:
    """Retrieves panelist name, slug string and average scores for each
    year"""
    if (
        use_decimal_scores
        and not current_app.config["app_settings"]["has_decimal_scores_column"]
    ):
        return None

    if not database_connection.is_connected():
        database_connection.reconnect()

    # Retrieve available panelists
    cursor = database_connection.cursor(named_tuple=True)
    query = """
        SELECT panelist AS name, panelistslug AS slug
        FROM ww_panelists
        WHERE panelistslug = %s
        ORDER BY panelistslug ASC;
        """
    cursor.execute(query, (panelist_slug,))
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return None

    panelist = {
        "name": result.name,
        "slug": result.slug,
    }

    if use_decimal_scores:
        query = """
            SELECT YEAR(s.showdate) AS year, SUM(pm.panelistscore_decimal) AS total,
            COUNT(pm.panelistscore_decimal) AS count
            FROM ww_showpnlmap pm
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE p.panelistslug = %s
            AND s.bestof = 0 AND s.repeatshowid IS NULL
            AND pm.panelistscore_decimal IS NOT NULL
            AND s.showdate <> '2018-10-27'
            GROUP BY YEAR(s.showdate)
            ORDER BY YEAR(s.showdate) ASC;
            """
    else:
        query = """
            SELECT YEAR(s.showdate) AS year, SUM(pm.panelistscore) AS total,
            COUNT(pm.panelistscore) AS count
            FROM ww_showpnlmap pm
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE p.panelistslug = %s
            AND s.bestof = 0 AND s.repeatshowid IS NULL
            AND pm.panelistscore IS NOT NULL
            AND s.showdate <> '2018-10-27'
            GROUP BY YEAR(s.showdate)
            ORDER BY YEAR(s.showdate) ASC;
            """
    cursor = database_connection.cursor(named_tuple=True)
    cursor.execute(query, (panelist["slug"],))
    result = cursor.fetchall()
    cursor.close()

    averages = empty_years_average(database_connection=database_connection).copy()
    if not result:
        panelist["averages"] = averages

    for row in result:
        if row.total and row.count:
            if use_decimal_scores:
                averages[row.year] = Decimal(Decimal(row.total) / Decimal(row.count))
            else:
                averages[row.year] = round(int(row.total) / int(row.count), 4)

    panelist["averages"] = averages
    return panelist


def retrieve_all_panelists_yearly_average(
    database_connection: mysql.connector.connect, use_decimal_scores: bool = False
) -> List[Dict]:
    """Retrieves a list of dictionaries for each panelist with panelist
    name, slug string and dictionary containing average scores for
    each year"""
    if (
        use_decimal_scores
        and not current_app.config["app_settings"]["has_decimal_scores_column"]
    ):
        return None

    if not database_connection.is_connected():
        database_connection.reconnect()

    # Retrieve available panelists
    cursor = database_connection.cursor(named_tuple=True)
    query = """
        SELECT panelist AS name, panelistslug AS slug
        FROM ww_panelists
        WHERE panelistslug <> 'multiple'
        ORDER BY panelistslug ASC;
        """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    # Retrieve panelist information and calculate average scores per year
    panelists = []
    for panelist in result:
        panelists.append(
            retrieve_panelist_yearly_average(
                panelist.slug,
                database_connection=database_connection,
                use_decimal_scores=use_decimal_scores,
            )
        )

    return panelists
