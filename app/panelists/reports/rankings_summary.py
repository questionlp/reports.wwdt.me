# Copyright (c) 2018-2024 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""WWDTM Panelist Rankings Summary Report Functions."""
from typing import Any

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from . import common


def retrieve_rankings_by_panelist(
    panelist_id: int, database_connection: MySQLConnection | PooledMySQLConnection
) -> dict[str, Any]:
    """Retrieves ranking statistics for the requested panelist."""
    if not database_connection.is_connected():
        database_connection.reconnect()

    query = """
        SELECT (
        SELECT COUNT(pm.showpnlrank) FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        WHERE pm.panelistid = %s AND pm.showpnlrank = '1' AND
        s.bestof = 0 and s.repeatshowid IS NULL) AS first, (
        SELECT COUNT(pm.showpnlrank) FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        WHERE pm.panelistid = %s AND pm.showpnlrank = '1t' AND
        s.bestof = 0 and s.repeatshowid IS NULL) AS first_tied, (
        SELECT COUNT(pm.showpnlrank) FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        WHERE pm.panelistid = %s AND pm.showpnlrank = '2' AND
        s.bestof = 0 and s.repeatshowid IS NULL) AS second, (
        SELECT COUNT(pm.showpnlrank) FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        WHERE pm.panelistid = %s AND pm.showpnlrank = '2t' AND
        s.bestof = 0 and s.repeatshowid IS NULL) AS second_tied, (
        SELECT COUNT(pm.showpnlrank) FROM ww_showpnlmap pm
        JOIN ww_shows s ON s.showid = pm.showid
        WHERE pm.panelistid = %s AND pm.showpnlrank = '3' AND
        s.bestof = 0 and s.repeatshowid IS NULL
        ) AS third;
        """
    cursor = database_connection.cursor(dictionary=True)
    cursor.execute(
        query,
        (
            panelist_id,
            panelist_id,
            panelist_id,
            panelist_id,
            panelist_id,
        ),
    )
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return None

    rankings = {
        "first": result["first"],
        "first_tied": result["first_tied"],
        "second": result["second"],
        "second_tied": result["second_tied"],
        "third": result["third"],
        "count": result["first"]
        + result["first_tied"]
        + result["second"]
        + result["second_tied"]
        + result["third"],
    }

    if rankings["count"]:
        rankings["percent_first"] = round(
            100 * (rankings["first"] / rankings["count"]), 5
        )
        rankings["percent_first_tied"] = round(
            100 * (rankings["first_tied"] / rankings["count"]), 5
        )
        rankings["percent_second"] = round(
            100 * (rankings["second"] / rankings["count"]), 5
        )
        rankings["percent_second_tied"] = round(
            100 * (rankings["second_tied"] / rankings["count"]), 5
        )
        rankings["percent_third"] = round(
            100 * (rankings["third"] / rankings["count"]), 5
        )

    return rankings


def retrieve_all_panelist_rankings(
    database_connection: MySQLConnection | PooledMySQLConnection,
) -> dict[str, Any]:
    """Returns ranking statistics for all available panelists."""
    panelists = common.retrieve_panelists(database_connection=database_connection)
    if not panelists:
        return None

    panelist_rankings = {}
    for panelist in panelists:
        panelist_id = panelist["id"]
        rankings = retrieve_rankings_by_panelist(
            panelist_id=panelist_id, database_connection=database_connection
        )
        panelist_rankings[panelist["slug"]] = rankings

    return panelist_rankings
