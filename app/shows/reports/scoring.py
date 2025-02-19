# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
# pylint: disable=C0301
"""WWDTM Show Scoring Reports Functions."""

from decimal import Decimal

from flask import current_app
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection


def retrieve_show_details(
    show_id: int,
    database_connection: MySQLConnection | PooledMySQLConnection,
    use_decimal_scores: bool = False,
) -> dict:
    """Retrieves host, scorekeeper, panelist, guest and location information."""
    if (
        use_decimal_scores
        and not current_app.config["app_settings"]["has_decimal_scores_column"]
    ):
        return None

    if not database_connection.is_connected():
        database_connection.reconnect()

    # Retrieve host and scorekeeper
    cursor = database_connection.cursor(dictionary=True)
    query = """
        SELECT s.showdate, h.host, sk.scorekeeper
        FROM ww_shows s
        JOIN ww_showhostmap hm on hm.showid = s.showid
        JOIN ww_hosts h ON h.hostid = hm.hostid
        JOIN ww_showskmap skm ON skm.showid = hm.showid
        JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid
        WHERE hm.showid = %s;
    """
    cursor.execute(query, (show_id,))
    result = cursor.fetchone()

    if not result:
        return None

    show_details = {
        "date": result["showdate"].isoformat(),
        "host": result["host"],
        "scorekeeper": result["scorekeeper"],
    }

    # Retrieve guest details
    query = """
        SELECT g.guest, gm.guestscore, gm.exception
        FROM ww_showguestmap gm
        JOIN ww_guests g ON g.guestid = gm.guestid
        JOIN ww_shows s ON s.showid = gm.showid
        WHERE gm.showid = %s;
    """
    cursor.execute(query, (show_id,))
    result = cursor.fetchall()

    if not result:
        show_details["guests"] = None
    else:
        guests = []
        for row in result:
            guests.append(
                {
                    "name": row["guest"],
                    "score": row["guestscore"],
                    "exception": bool(row["exception"]),
                }
            )

        show_details["guests"] = guests

    # Retrieve show location details
    query = """
        SELECT l.city, l.state, l.venue
        FROM ww_showlocationmap lm
        JOIN ww_locations l ON l.locationid = lm.locationid
        WHERE lm.showid = %s;
    """
    cursor.execute(query, (show_id,))
    result = cursor.fetchone()

    if not result:
        show_details["location"] = None
    else:
        show_details["location"] = {
            "city": result["city"],
            "state": result["state"],
            "venue": result["venue"],
        }

    # Retrieve panelists and their respective show rank and score
    if use_decimal_scores:
        query = """
            SELECT p.panelist, pm.panelistscore, pm.panelistscore_decimal
            FROM ww_showpnlmap pm
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            WHERE pm.showid = %s
            ORDER BY pm.panelistscore_decimal DESC, pm.showpnlrank ASC;
        """
    else:
        query = """
            SELECT p.panelist, pm.panelistscore
            FROM ww_showpnlmap pm
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            WHERE pm.showid = %s
            ORDER BY pm.panelistscore DESC, pm.showpnlrank ASC;
        """
    cursor.execute(query, (show_id,))
    result = cursor.fetchall()
    cursor.close()

    if not result:
        show_details["panelists"] = None
    else:
        panelists = []
        for row in result:
            if use_decimal_scores:
                panelists.append(
                    {
                        "name": row["panelist"],
                        "score": row["panelistscore"],
                        "score_decimal": row["panelistscore_decimal"],
                    }
                )
            else:
                panelists.append(
                    {
                        "name": row["panelist"],
                        "score": row["panelistscore"],
                    }
                )

        show_details["panelists"] = panelists

    return show_details


def retrieve_shows_all_high_scoring(
    database_connection: MySQLConnection | PooledMySQLConnection,
    use_decimal_scores: bool = False,
) -> list[dict]:
    """Retrieves details from shows with a panelist total score greater than or equal to 50."""
    if (
        use_decimal_scores
        and not current_app.config["app_settings"]["has_decimal_scores_column"]
    ):
        return None

    if not database_connection.is_connected():
        database_connection.reconnect()

    if use_decimal_scores:
        query = """
            SELECT s.showid, s.showdate, SUM(pm.panelistscore_decimal) AS total
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE s.bestof = 0 AND s.repeatshowid IS NULL
            GROUP BY s.showid
            HAVING SUM(pm.panelistscore_decimal) >= 50
            ORDER BY SUM(pm.panelistscore_decimal) DESC, s.showdate DESC;
        """
    else:
        query = """
            SELECT s.showid, s.showdate, SUM(pm.panelistscore) AS total
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE s.bestof = 0 AND s.repeatshowid IS NULL
            GROUP BY s.showid
            HAVING SUM(pm.panelistscore) >= 50
            ORDER BY SUM(pm.panelistscore) DESC, s.showdate DESC;
        """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    shows = []
    for row in result:
        show_id = row["showid"]
        show_details = retrieve_show_details(
            show_id, database_connection, use_decimal_scores=use_decimal_scores
        )

        if show_details:
            if use_decimal_scores:
                show_details["total_score"] = Decimal(row["total"])
            else:
                show_details["total_score"] = row["total"]

            if show_details:
                shows.append(show_details)

    return shows


def retrieve_shows_all_low_scoring(
    database_connection: MySQLConnection | PooledMySQLConnection,
    use_decimal_scores: bool = False,
) -> list[dict]:
    """Retrieves details from shows with a panelist total score of less than 30.

    Excludes the 20th anniversary show due to unique Lightning
    Fill-in-the-Blank segment.
    """
    if (
        use_decimal_scores
        and not current_app.config["app_settings"]["has_decimal_scores_column"]
    ):
        return None

    if not database_connection.is_connected():
        database_connection.reconnect()

    if use_decimal_scores:
        query = """
            SELECT s.showid, s.showdate, SUM(pm.panelistscore_decimal) AS total
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE s.bestof = 0 AND s.repeatshowid IS NULL
            AND s.showdate <> '2018-10-27'
            GROUP BY s.showid
            HAVING SUM(pm.panelistscore_decimal) < 30
            ORDER BY SUM(pm.panelistscore_decimal) ASC, s.showdate DESC;
        """
    else:
        query = """
            SELECT s.showid, s.showdate, SUM(pm.panelistscore) AS total
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            WHERE s.bestof = 0 AND s.repeatshowid IS NULL
            AND s.showdate <> '2018-10-27'
            GROUP BY s.showid
            HAVING SUM(pm.panelistscore) < 30
            ORDER BY SUM(pm.panelistscore) ASC, s.showdate DESC;
        """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    shows = []
    for row in result:
        show_id = row["showid"]
        show_details = retrieve_show_details(
            show_id, database_connection, use_decimal_scores=use_decimal_scores
        )

        if show_details:
            if use_decimal_scores:
                show_details["total_score"] = Decimal(row["total"])
            else:
                show_details["total_score"] = row["total"]

            if show_details:
                shows.append(show_details)

    return shows


def retrieve_shows_panelist_score_sum_match(
    database_connection: MySQLConnection | PooledMySQLConnection,
    use_decimal_scores: bool = False,
) -> list[dict]:
    """Retrieves shows where a panelist's first place score matches the sum of the scores of the other two panelists.

    Excludes the 20th anniversary show due to unique Lightning
    Fill-in-the-Blank segment.
    """
    if (
        use_decimal_scores
        and not current_app.config["app_settings"]["has_decimal_scores_column"]
    ):
        return None

    if not database_connection.is_connected():
        database_connection.reconnect()

    if use_decimal_scores:
        query = """
            SELECT s.showdate, pm.panelistid, p.panelist, p.panelistslug,
            pm.panelistscore, pm.panelistscore_decimal, pm.showpnlrank
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            WHERE s.bestof = 0 AND s.repeatshowid IS NULL AND
            s.showdate <> '2018-10-27' AND
            pm.panelistscore_decimal IS NOT NULL
            ORDER BY s.showdate ASC, pm.panelistscore_decimal DESC;
        """
    else:
        query = """
            SELECT s.showdate, pm.panelistid, p.panelist, p.panelistslug,
            pm.panelistscore, pm.showpnlrank
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            WHERE s.bestof = 0 AND s.repeatshowid IS NULL AND
            s.showdate <> '2018-10-27' AND
            pm.panelistscore IS NOT NULL
            ORDER BY s.showdate ASC, pm.panelistscore DESC;
        """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    shows = {}
    for row in result:
        show_date = row["showdate"].isoformat()
        if show_date not in shows:
            shows[show_date] = []

        if use_decimal_scores:
            shows[show_date].append(
                {
                    "panelist_id": row["panelistid"],
                    "panelist": row["panelist"],
                    "panelist_slug": row["panelistslug"],
                    "score": row["panelistscore"],
                    "score_decimal": row["panelistscore_decimal"],
                    "rank": row["showpnlrank"],
                }
            )
        else:
            shows[show_date].append(
                {
                    "panelist_id": row["panelistid"],
                    "panelist": row["panelist"],
                    "panelist_slug": row["panelistslug"],
                    "score": row["panelistscore"],
                    "rank": row["showpnlrank"],
                }
            )

    shows_match = {}
    for show in shows:
        if use_decimal_scores:
            show_info = shows[show]
            score_1 = show_info[0]["score_decimal"]
            score_2 = show_info[1]["score_decimal"]
            score_3 = show_info[2]["score_decimal"]
            if score_1 == score_2 + score_3:
                shows_match[show] = show_info
        else:
            show_info = shows[show]
            score_1 = show_info[0]["score"]
            score_2 = show_info[1]["score"]
            score_3 = show_info[2]["score"]
            if score_1 == score_2 + score_3:
                shows_match[show] = show_info

    return shows_match


def retrieve_shows_panelist_perfect_scores(
    database_connection: MySQLConnection | PooledMySQLConnection,
    use_decimal_scores: bool = False,
) -> list[dict[str, str | int]]:
    """Retrieves shows in which a panelist scores a total of 20 points or higher.

    Best Of and repeat shows are excluded.
    """
    if (
        use_decimal_scores
        and not current_app.config["app_settings"]["has_decimal_scores_column"]
    ):
        return None

    if not database_connection.is_connected():
        database_connection.reconnect()

    if use_decimal_scores:
        query = """
            SELECT s.showdate, p.panelist, p.panelistslug,
            pm.panelistscore, pm.panelistscore_decimal
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            WHERE pm.panelistscore_decimal >= 20
            AND s.bestof = 0 AND s.repeatshowid IS NULL
            ORDER BY s.showdate ASC;
        """
    else:
        query = """
            SELECT s.showdate, p.panelist, p.panelistslug,
            pm.panelistscore
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            WHERE pm.panelistscore >= 20
            AND s.bestof = 0 AND s.repeatshowid IS NULL
            ORDER BY s.showdate ASC;
        """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()

    if not result:
        return None

    shows = []
    for row in result:
        if use_decimal_scores:
            shows.append(
                {
                    "date": row["showdate"],
                    "panelist": row["panelist"],
                    "panelist_slug": row["panelistslug"],
                    "score": row["panelistscore"],
                    "score_decimal": row["panelistscore_decimal"],
                }
            )
        else:
            shows.append(
                {
                    "date": row["showdate"],
                    "panelist": row["panelist"],
                    "panelist_slug": row["panelistslug"],
                    "score": row["panelistscore"],
                }
            )

    return shows
