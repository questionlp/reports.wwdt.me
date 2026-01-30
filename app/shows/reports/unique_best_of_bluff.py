# Copyright (c) 2018-2026 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Unique Best Of Bluff the Listener Segments Report Functions."""

from curses import panel
from typing import Any

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from app.panelists.reports.common import retrieve_panelists_id_key

from .show_details import retrieve_show_date_by_id


def retrieve_unique_best_of_bluff_shows(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> list[dict[str, Any]]:
    """Retrieves a list of Best Of shows with a unique Bluff the Listener Segment."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT s.showdate, s.repeatshowid, blm.segment, blm.chosenbluffpnlid,
        blm.correctbluffpnlid
        FROM ww_showbluffmap blm
        JOIN ww_shows s ON s.showid = blm.showid
        WHERE s.bestof = 1 AND s.bestofuniquebluff = 1
        ORDER BY s.showdate ASC;
    """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()

    if not results:
        return None

    panelists = retrieve_panelists_id_key(database_connection=database_connection)
    shows = []

    for row in results:
        _repeat_show = bool(row["repeatshowid"])
        shows.append(
            {
                "date": row["showdate"].isoformat(),
                "repeat": _repeat_show,
                "original_show_date": retrieve_show_date_by_id(row["repeatshowid"])
                if _repeat_show
                else None,
                "bluff_segment": row["segment"],
                "chosen_bluff": panelists[row["chosenbluffpnlid"]]
                if row["chosenbluffpnlid"]
                else None,
                "correct_bluff": panelists[row["correctbluffpnlid"]]
                if row["correctbluffpnlid"]
                else None,
            }
        )

    return shows
