# Copyright (c) 2018-2024 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Panel Gender Mix Report Functions."""
from decimal import Decimal
from typing import Any

import numpy
from flask import current_app
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection


def retrieve_show_years(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[int]:
    """Retrieve a list of available show years."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
    SELECT DISTINCT YEAR(showdate)
    FROM ww_shows
    ORDER BY YEAR(showdate) ASC;
    """
    cursor = database_connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    return [row[0] for row in result]


def retrieve_scores_by_year_gender(
    year: int,
    gender: str,
    database_connection: MySQLConnection | PooledMySQLConnection,
    use_decimal_scores: bool = False,
) -> list[int | Decimal]:
    """Retrieve a list of panelist scores for a given year and panelists of the requested gender."""
    if (
        use_decimal_scores
        and not current_app.config["app_settings"]["has_decimal_scores_column"]
    ):
        return None

    if not gender:
        return None

    panelist_gender = gender[0].upper()

    if not database_connection.is_connected():
        database_connection.reconnect()

    if use_decimal_scores:
        query = """
            SELECT pm.panelistscore_decimal AS score FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            WHERE s.bestof = 0 AND s.repeatshowid IS NULL
            AND pm.panelistscore IS NOT NULL
            AND p.panelistgender = %s
            AND YEAR(s.showdate) = %s
            ORDER BY s.showdate ASC;
            """
    else:
        query = """
            SELECT pm.panelistscore AS score FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            WHERE s.bestof = 0 AND s.repeatshowid IS NULL
            AND pm.panelistscore IS NOT NULL
            AND p.panelistgender = %s
            AND YEAR(s.showdate) = %s
            ORDER BY s.showdate ASC;
            """
    cursor = database_connection.cursor(named_tuple=True)
    cursor.execute(query, (panelist_gender, year))
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    return [row.score for row in result]


def retrieve_stats_by_year_gender(
    database_connection: MySQLConnection | PooledMySQLConnection,
    use_decimal_scores: bool = False,
) -> dict[str, Any]:
    """Retrieve statistics about panelist scores broken out by year and gender."""
    if (
        use_decimal_scores
        and not current_app.config["app_settings"]["has_decimal_scores_column"]
    ):
        return None

    show_years = retrieve_show_years(database_connection)

    all_stats = {}
    for year in show_years:
        all_stats[year] = {}
        for gender in ["F", "M"]:
            scores = retrieve_scores_by_year_gender(
                year=year,
                gender=gender,
                database_connection=database_connection,
                use_decimal_scores=use_decimal_scores,
            )
            if scores:
                if use_decimal_scores:
                    all_stats[year][gender] = {
                        "minimum": Decimal(numpy.amin(scores)),
                        "maximum": Decimal(numpy.amax(scores)),
                        "mean": round(Decimal(numpy.mean(scores)), 5),
                        "median": Decimal(numpy.median(scores)),
                        "standard_deviation": round(Decimal(numpy.std(scores)), 5),
                        "count": Decimal(len(scores)),
                        "total": Decimal(numpy.sum(scores)),
                    }
                else:
                    all_stats[year][gender] = {
                        "minimum": int(numpy.amin(scores)),
                        "maximum": int(numpy.amax(scores)),
                        "mean": round(numpy.mean(scores), 5),
                        "median": int(numpy.median(scores)),
                        "standard_deviation": round(numpy.std(scores), 5),
                        "count": len(scores),
                        "total": int(numpy.sum(scores)),
                    }
            else:
                all_stats[year][gender] = None

    return all_stats
