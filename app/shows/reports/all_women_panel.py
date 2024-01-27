# Copyright (c) 2018-2024 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM All Women Panel Report Functions."""
from flask import current_app
from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection


def retrieve_show_details(
    show_id: int,
    database_connection: MySQLConnection | PooledMySQLConnection,
    use_decimal_scores: bool = False,
) -> dict:
    """Retrieves host, scorekeeper, panelist, guest and location information for the requested show ID."""
    if (
        use_decimal_scores
        and not current_app.config["app_settings"]["has_decimal_scores_column"]
    ):
        return None

    if not database_connection.is_connected():
        database_connection.reconnect()

    # Retrieve host, scorekeeper and guest
    query = """
        SELECT s.showdate, h.host, sk.scorekeeper, g.guest,
        gm.guestscore, gm.exception
        FROM ww_showhostmap hm
        JOIN ww_shows s ON s.showid = hm.showid
        JOIN ww_hosts h ON h.hostid = hm.hostid
        JOIN ww_showskmap skm ON skm.showid = hm.showid
        JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid
        JOIN ww_showguestmap gm ON gm.showid = hm.showid
        JOIN ww_guests g ON g.guestid = gm.guestid
        WHERE hm.showid = %s;
        """
    cursor = database_connection.cursor(named_tuple=True)
    cursor.execute(query, (show_id,))
    result = cursor.fetchone()

    if not result:
        return None

    show_details = {
        "date": result.showdate.isoformat(),
        "host": result.host,
        "scorekeeper": result.scorekeeper,
        "guest": {
            "name": result.guest,
            "score": result.guestscore,
            "exception": bool(result.exception),
        },
    }

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
            "city": result.city,
            "state": result.state,
            "venue": result.venue,
        }

    # Retrieve panelists and their respective show rank and score
    if use_decimal_scores:
        query = """
            SELECT p.panelist, pm.panelistscore, pm.panelistscore_decimal
            FROM ww_showpnlmap pm
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            WHERE pm.showid = %s
            ORDER BY pm.panelistscore DESC, pm.showpnlrank ASC;
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
                        "name": row.panelist,
                        "score": row.panelistscore,
                        "score_decimal": row.panelistscore_decimal,
                    }
                )
            else:
                panelists.append(
                    {
                        "name": row.panelist,
                        "score": row.panelistscore,
                    }
                )

        show_details["panelists"] = panelists

    return show_details


def retrieve_shows_all_women_panel(
    database_connection: MySQLConnection | PooledMySQLConnection,
    use_decimal_scores: bool = False,
) -> list[dict]:
    """Retrieves details from all shows that have had an all women panel."""
    if (
        use_decimal_scores
        and not current_app.config["app_settings"]["has_decimal_scores_column"]
    ):
        return None

    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT pm.showid
        FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        JOIN ww_panelists p ON p.panelistid = pm.panelistid
        WHERE s.bestof = 0 AND s.repeatshowid IS NULL
        AND s.showdate <> '2018-10-27'
        AND p.panelistgender = 'F'
        GROUP BY pm.showid
        HAVING COUNT(s.showid) = 3
        ORDER BY s.showdate ASC;
        """
    cursor = database_connection.cursor(named_tuple=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    shows = []
    for row in result:
        show_id = row.showid
        show_details = retrieve_show_details(
            show_id, database_connection, use_decimal_scores=use_decimal_scores
        )
        if show_details:
            shows.append(show_details)

    return shows
