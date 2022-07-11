# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Hosts Appearances Report Functions"""
from typing import Any, Dict, List

import mysql.connector


def retrieve_hosts(
    database_connection: mysql.connector.connect,
) -> List[Dict[str, str]]:
    """Retrieves a dictionary for all available hosts from the database"""

    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT h.hostid, h.host, h.hostslug "
        "FROM ww_hosts h "
        "WHERE h.host <> '(TBD)' "
        "ORDER BY h.hostslug ASC;"
    )
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    _hosts = []
    for row in result:
        _hosts.append(
            {
                "name": row.host,
                "slug": row.hostslug,
            }
        )

    return _hosts


def retrieve_appearances_by_host(
    host_slug: str, database_connection: mysql.connector.connect
) -> Dict[str, int]:
    """Retrieve appearance data for the requested host"""

    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT ( "
        "SELECT COUNT(hm.showid) FROM ww_showhostmap hm "
        "JOIN ww_shows s ON s.showid = hm.showid "
        "JOIN ww_hosts h ON h.hostid = hm.hostid "
        "WHERE s.bestof = 0 AND s.repeatshowid IS NULL AND "
        "h.hostslug = %s ) AS regular, ( "
        "SELECT COUNT(hm.showid) FROM ww_showhostmap hm "
        "JOIN ww_shows s ON s.showid = hm.showid "
        "JOIN ww_hosts h ON h.hostid = hm.hostid "
        "WHERE h.hostslug = %s ) AS allshows;"
    )
    cursor.execute(
        query,
        (
            host_slug,
            host_slug,
        ),
    )
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return None

    return {
        "regular": result.regular,
        "all": result.allshows,
    }


def retrieve_first_most_recent_appearances(
    host_slug: str, database_connection: mysql.connector.connect
) -> Dict[str, str]:
    """Retrieve first and most recent appearances for both regular
    and all shows for the requested host"""

    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT MIN(s.showdate) AS min, MAX(s.showdate) AS max "
        "FROM ww_showhostmap hm "
        "JOIN ww_shows s ON s.showid = hm.showid "
        "JOIN ww_hosts h ON h.hostid = hm.hostid "
        "WHERE h.hostslug = %s "
        "AND s.bestof = 0 "
        "AND s.repeatshowid IS null;"
    )
    cursor.execute(query, (host_slug,))
    result = cursor.fetchone()
    cursor.close()

    if not result:
        return None

    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT MIN(s.showdate) AS min, MAX(s.showdate) AS max "
        "FROM ww_showhostmap hm "
        "JOIN ww_shows s ON s.showid = hm.showid "
        "JOIN ww_hosts h ON h.hostid = hm.hostid "
        "WHERE h.hostslug = %s;"
    )
    cursor.execute(query, (host_slug,))
    result_all = cursor.fetchone()
    cursor.close()

    if not result:
        return {
            "first": result.min.isoformat(),
            "most_recent": result.max.isoformat(),
        }

    return {
        "first": result.min.isoformat(),
        "most_recent": result.max.isoformat(),
        "first_all": result_all.min.isoformat(),
        "most_recent_all": result_all.max.isoformat(),
    }


def retrieve_appearance_summaries(
    database_connection: mysql.connector.connect,
) -> List[Dict[str, Any]]:
    """Retrieve host appearance summary, including appearance counts,
    and first and most recent appearances"""

    if not database_connection.is_connected():
        database_connection.reconnect()

    _hosts = retrieve_hosts(database_connection=database_connection)

    if not _hosts:
        return None

    hosts_summary = {}
    for host in _hosts:
        appearance_count = retrieve_appearances_by_host(
            host_slug=host["slug"], database_connection=database_connection
        )
        first_most_recent = retrieve_first_most_recent_appearances(
            host_slug=host["slug"], database_connection=database_connection
        )
        hosts_summary[host["slug"]] = {
            "slug": host["slug"],
            "name": host["name"],
            "regular_shows": appearance_count["regular"],
            "all_shows": appearance_count["all"],
            "first": first_most_recent["first"],
            "first_all": first_most_recent["first_all"],
            "most_recent": first_most_recent["most_recent"],
            "most_recent_all": first_most_recent["most_recent_all"],
        }

    return hosts_summary
