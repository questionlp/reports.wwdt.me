# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Panelist Show Appearances Report Functions."""

from typing import Any

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from app.shows.reports.show_details import (
    retrieve_show_date_by_id,
    retrieve_show_guests,
    retrieve_show_panelists_details,
)


def retrieve_appearance_details(
    panelist_slug: str,
    year: int,
    database_connection: MySQLConnection | PooledMySQLConnection,
    include_decimal_scores: bool = False,
) -> list[dict[str, Any]]:
    """Retrieves details for all appearances for a given panelist and year.

    Returned information includes show date, show flags, location,
    host, scorekeeper, panelist scoring information, other panelists,
    and Not My Job guest(s).
    """
    if not database_connection.is_connected():
        database_connection.reconnect()

    if include_decimal_scores:
        query = """
            SELECT s.showid, s.showdate, s.bestof, s.repeatshowid,
            l.venue, l.city, l.state, h.host, h.hostslug,
            sk.scorekeeper, sk.scorekeeperslug, p.panelist,
            pm.panelistlrndstart, pm.panelistlrndstart_decimal,
            pm.panelistlrndcorrect, pm.panelistlrndcorrect_decimal,
            pm.panelistscore, pm.panelistscore_decimal,
            pm.showpnlrank
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            JOIN ww_showhostmap hm ON hm.showid = pm.showid
            JOIN ww_hosts h ON h.hostid = hm.hostid
            JOIN ww_showskmap skm ON skm.showid = pm.showid
            JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid
            JOIN ww_showlocationmap lm ON lm.showid = pm.showid
            JOIN ww_locations l on l.locationid = lm.locationid
            WHERE p.panelistslug = %s AND YEAR(s.showdate) = %s
            ORDER BY s.showdate ASC;
        """
    else:
        query = """
            SELECT s.showid, s.showdate, s.bestof, s.repeatshowid,
            l.venue, l.city, l.state, h.host, h.hostslug,
            sk.scorekeeper, sk.scorekeeperslug, p.panelist,
            pm.panelistlrndstart, pm.panelistlrndcorrect, pm.panelistscore,
            pm.showpnlrank
            FROM ww_showpnlmap pm
            JOIN ww_shows s ON s.showid = pm.showid
            JOIN ww_panelists p ON p.panelistid = pm.panelistid
            JOIN ww_showhostmap hm ON hm.showid = pm.showid
            JOIN ww_hosts h ON h.hostid = hm.hostid
            JOIN ww_showskmap skm ON skm.showid = pm.showid
            JOIN ww_scorekeepers sk ON sk.scorekeeperid = skm.scorekeeperid
            JOIN ww_showlocationmap lm ON lm.showid = pm.showid
            JOIN ww_locations l on l.locationid = lm.locationid
            WHERE p.panelistslug = %s AND YEAR(s.showdate) = %s
            ORDER BY s.showdate ASC;
        """

    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(
        query,
        (
            panelist_slug,
            year,
        ),
    )
    results = cursor.fetchall()
    cursor.close()

    if not results:
        return None

    _appearances = []
    for row in results:
        _panelists = retrieve_show_panelists_details(
            show_id=row["showid"],
            database_connection=database_connection,
            include_decimal_scores=include_decimal_scores,
        )
        _other_panelists = []
        if _panelists:
            for _other_panelist in _panelists:
                if _other_panelist["slug"] != panelist_slug:
                    _other_panelists.append(_other_panelist)

        _guests = retrieve_show_guests(
            show_id=row["showid"], database_connection=database_connection
        )

        _show_info = {
            "date": row["showdate"].isoformat(),
            "best_of": bool(row["bestof"]),
            "repeat": bool(row["repeatshowid"]),
            "original_show_date": (
                retrieve_show_date_by_id(
                    show_id=row["repeatshowid"], database_connection=database_connection
                )
                if row["repeatshowid"]
                else None
            ),
            "location": {
                "venue": row["venue"],
                "city": row["city"],
                "state": row["state"],
            },
            "host": {
                "name": row["host"],
                "slug": row["hostslug"],
            },
            "scorekeeper": {
                "name": row["scorekeeper"],
                "slug": row["scorekeeperslug"],
            },
            "scoring": {
                "start": row["panelistlrndstart"],
                "start_decimal": (
                    row["panelistlrndstart_decimal"] if include_decimal_scores else None
                ),
                "correct": row["panelistlrndcorrect"],
                "correct_decimal": (
                    row["panelistlrndcorrect_decimal"]
                    if include_decimal_scores
                    else None
                ),
                "score": row["panelistscore"],
                "score_decimal": (
                    row["panelistscore_decimal"] if include_decimal_scores else None
                ),
                "rank": row["showpnlrank"],
            },
            "other_panelists": _other_panelists,
            "guests": _guests,
        }

        _appearances.append(_show_info)

    return _appearances
