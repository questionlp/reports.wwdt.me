# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
# pylint: disable=C0301
"""WWDTM Lightning Fill-in-the-Blank Segment Report Functions."""

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection


def retrieve_all_lightning_round_start(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> dict:
    """Retrieve a dictionary of all Lightning Fill-in-the-Blank round starting scores."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT s.showid, s.showdate, p.panelistid, p.panelist,
        pm.panelistlrndstart_decimal
        FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        WHERE s.bestof = 0 AND s.repeatshowid IS NULL
        AND s.showdate <> '2018-10-27' -- Excluding 25th anniversary special
        AND pm.panelistlrndstart_decimal IS NOT NULL
        ORDER BY s.showdate ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    show_lightning_round_starts = {}
    for row in result:
        show_id = row["showid"]
        if show_id not in show_lightning_round_starts:
            show_lightning_round_starts[show_id] = {
                "id": show_id,
                "date": row["showdate"].isoformat(),
                "scores": [],
            }

        show_lightning_round_starts[show_id]["scores"].append(
            row["panelistlrndstart_decimal"]
        )

    return show_lightning_round_starts


def retrieve_scoring_info_by_show_id(
    show_id: int,
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> dict:
    """Return Lightning Fill-in-the-Blank round scoring information.

    Returned information includes starting points, number of correct
    answers and final score for the requested show ID. Used for
    getting scoring details where the round starts in a three-way tie.
    """
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT s.showdate, pm.panelistlrndstart_decimal,
        pm.panelistlrndcorrect_decimal, pm.panelistscore_decimal
        FROM ww_shows s
        JOIN ww_showpnlmap pm ON pm.showid = s.showid
        WHERE s.showid = %s
        LIMIT 1;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (show_id,))
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return None

    return {
        "id": show_id,
        "date": result["showdate"].isoformat(),
        "start": result["panelistlrndstart_decimal"],
        "correct": result["panelistlrndcorrect_decimal"],
        "score": result["panelistscore_decimal"],
    }


def retrieve_panelists_by_show_id(
    show_id: int,
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict]:
    """Returns a list of panelists for the requested show ID."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT p.panelistid, p.panelist, p.panelistslug
        FROM ww_showpnlmap pm
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        JOIN ww_shows s ON s.showid = pm.showid
        WHERE s.showid = %s
        ORDER BY pm.showpnlmapid ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query, (show_id,))
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    panelists = []
    for row in result:
        panelists.append(
            {
                "id": row["panelistid"],
                "name": row["panelist"],
                "slug": row["panelistslug"],
            }
        )

    return panelists


def shows_with_lightning_round_start_zero(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict]:
    """Return shows in which panelists start the Lightning round with zero points."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT s.showid, s.showdate, p.panelistid, p.panelist,
        pm.panelistlrndstart_decimal, pm.panelistlrndcorrect_decimal,
        pm.panelistscore_decimal, pm.showpnlrank
        FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        WHERE s.bestof = 0 AND s.repeatshowid IS NULL
        AND pm.panelistlrndstart_decimal = 0
        ORDER BY s.showdate ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    shows = []
    for row in result:
        shows.append(
            {
                "id": row["showid"],
                "date": row["showdate"].isoformat(),
                "panelist": {
                    "id": row["panelistid"],
                    "name": row["panelist"],
                    "start": row["panelistlrndstart_decimal"],
                    "correct": row["panelistlrndcorrect_decimal"],
                    "score": row["panelistscore_decimal"],
                    "rank": row["showpnlrank"],
                },
            }
        )

    return shows


def shows_lightning_round_start_zero(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict]:
    """Return list of shows in which a panelist starts the Lightning round with zero points."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT s.showid, s.showdate, p.panelistid, p.panelist,
        pm.panelistlrndstart_decimal, pm.panelistlrndcorrect_decimal,
        pm.panelistscore_decimal, pm.showpnlrank
        FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        WHERE s.bestof = 0 AND s.repeatshowid IS NULL
        AND pm.panelistlrndstart_decimal = 0
        ORDER BY s.showdate ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    shows = []
    for row in result:
        shows.append(
            {
                "id": row["showid"],
                "date": row["showdate"].isoformat(),
                "panelist": {
                    "id": row["panelistid"],
                    "name": row["panelist"],
                    "start": row["panelistlrndstart_decimal"],
                    "correct": row["panelistlrndcorrect_decimal"],
                    "score": row["panelistscore_decimal"],
                    "rank": row["showpnlrank"],
                },
            }
        )
    return shows


def shows_lightning_round_zero_correct(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict]:
    """Return list of shows in which a panelist answers zero Lightning round questions correct."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT s.showid, s.showdate, p.panelistid, p.panelist,
        pm.panelistlrndstart_decimal, pm.panelistlrndcorrect_decimal,
        pm.panelistscore_decimal, pm.showpnlrank
        FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        WHERE s.bestof = 0 AND s.repeatshowid IS null
        AND pm.panelistlrndcorrect_decimal = 0
        ORDER BY s.showdate ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    shows = []
    for row in result:
        shows.append(
            {
                "id": row["showid"],
                "date": row["showdate"].isoformat(),
                "panelist": {
                    "id": row["panelistid"],
                    "name": row["panelist"],
                    "start": row["panelistlrndstart_decimal"],
                    "correct": row["panelistlrndcorrect_decimal"],
                    "score": row["panelistscore_decimal"],
                    "rank": row["showpnlrank"],
                },
            }
        )

    return shows


def shows_lightning_round_answering_same_number_correct(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict]:
    """Return list of shows in which all panelists answers the same number of Lightning questions correct."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT s.showid, s.showdate, pm.panelistlrndcorrect_decimal,
        COUNT(pm.panelistlrndcorrect_decimal) AS count
        FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        WHERE s.bestof = 0 AND s.repeatshowid IS NULL
        AND pm.panelistlrndcorrect IS NOT NULL
        AND pm.panelistlrndcorrect_decimal IS NOT NULL
        GROUP BY s.showid, pm.panelistlrndcorrect,
        pm.panelistlrndcorrect_decimal
        HAVING COUNT(pm.panelistlrndcorrect_decimal) = 3
        ORDER BY s.showdate ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    shows = []
    for row in result:
        panelists = retrieve_panelists_by_show_id(
            show_id=row["showid"], database_connection=database_connection
        )
        shows.append(
            {
                "id": row["showid"],
                "date": row["showdate"].isoformat(),
                "panelists": panelists,
                "correct_decimal": row["panelistlrndcorrect_decimal"],
            }
        )

    return shows


def shows_starting_with_three_way_tie(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict]:
    """Retrieve all shows in which all three panelists started the Lightning round in a three-way tie."""
    show_scores = retrieve_all_lightning_round_start(
        database_connection=database_connection,
    )
    shows = []

    for show in show_scores:
        show_id = show_scores[show]["id"]
        show_date = show_scores[show]["date"]

        if len(set(show_scores[show]["scores"])) == 1:
            shows.append(
                {
                    "id": show_id,
                    "date": show_date,
                    "score": show_scores[show]["scores"][0],
                    "panelists": retrieve_panelists_by_show_id(
                        show_id=show_id, database_connection=database_connection
                    ),
                }
            )

    return shows


def shows_ending_with_three_way_tie(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict]:
    """Retrieve all shows in which all three panelists ended the Lightning round in a three-way tie."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT s.showid, s.showdate, pm.panelistscore_decimal,
        COUNT(pm.showpnlrank) AS count
        FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        WHERE s.bestof = 0 AND s.repeatshowid IS NULL
        AND pm.showpnlrank = '1t'
        GROUP BY s.showid, pm.panelistscore, pm.panelistscore_decimal
        HAVING COUNT(pm.showpnlrank) = 3
        ORDER BY s.showdate ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    shows = []
    for row in result:
        shows.append(
            {
                "id": row["showid"],
                "date": row["showdate"].isoformat(),
                "score": row["panelistscore_decimal"],
                "panelists": retrieve_panelists_by_show_id(
                    show_id=row["showid"], database_connection=database_connection
                ),
            }
        )

    return shows


def shows_starting_ending_three_way_tie(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict]:
    """Retrieve all shows in which all three panelists started and ended the Lightning round in a three-way tie."""
    start_tie = shows_starting_with_three_way_tie(database_connection)
    end_tie = shows_ending_with_three_way_tie(
        database_connection=database_connection,
    )

    if not start_tie or not end_tie:
        return None

    start_tie_ids = []
    end_tie_ids = []

    for start_tie_show in start_tie:
        start_tie_ids.append(start_tie_show["id"])

    for end_tie_show in end_tie:
        end_tie_ids.append(end_tie_show["id"])

    shows_intersect = set(start_tie_ids) & set(end_tie_ids)

    if not shows_intersect:
        return None

    show_info = []
    for show_id in shows_intersect:
        score_info = retrieve_scoring_info_by_show_id(
            show_id=show_id,
            database_connection=database_connection,
        )

        if score_info:
            show_info.append(
                {
                    "id": show_id,
                    "date": score_info["date"],
                    "panelists": retrieve_panelists_by_show_id(
                        show_id=show_id, database_connection=database_connection
                    ),
                    "start": score_info["start"],
                    "correct": score_info["correct"],
                    "score": score_info["score"],
                }
            )

    return show_info
