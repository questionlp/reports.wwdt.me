# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Hosts Appearances Report Functions"""
from typing import Any, Dict, List

from flask import current_app
import mysql.connector


def retrieve_all_hosts() -> List[Dict[str, str]]:
    """Retrieves a dictionary for all available hosts from the database"""

    database_connection = mysql.connector.connect(**current_app.config["database"])
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
    database_connection.close()

    if not result:
        return None

    _hosts = []
    for row in result:
        host = {}
        host["name"] = row.host
        host["slug"] = row.hostslug
        _hosts.append(host)

    return _hosts


def retrieve_appearances_by_host(host_slug: str) -> Dict[str, int]:
    """Retrieve appearance data for the requested host"""

    database_connection = mysql.connector.connect(**current_app.config["database"])
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
    database_connection.close()

    if not result:
        return None

    _appearances = {}
    _appearances["regular"] = result.regular
    _appearances["all"] = result.allshows

    return _appearances


def retrieve_first_most_recent_appearances(host_slug: str) -> Dict[str, str]:
    """Retrieve first and most recent appearances for both regular
    and all shows for the requested host"""

    database_connection = mysql.connector.connect(**current_app.config["database"])
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

    appearance_info = {}
    appearance_info["first"] = result.min.isoformat()
    appearance_info["most_recent"] = result.max.isoformat()

    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT MIN(s.showdate) AS min, MAX(s.showdate) AS max "
        "FROM ww_showhostmap hm "
        "JOIN ww_shows s ON s.showid = hm.showid "
        "JOIN ww_hosts h ON h.hostid = hm.hostid "
        "WHERE h.hostslug = %s;"
    )
    cursor.execute(query, (host_slug,))
    result = cursor.fetchone()
    cursor.close()
    database_connection.close()

    if not result:
        return appearance_info

    appearance_info["first_all"] = result.min.isoformat()
    appearance_info["most_recent_all"] = result.max.isoformat()

    return appearance_info


def retrieve_appearance_summaries() -> List[Dict[str, Any]]:
    """Retrieve host appearance summary, including appearance counts,
    and first and most recent appearances"""

    _hosts = retrieve_all_hosts()

    if not _hosts:
        return None

    hosts_summary = {}
    for host in _hosts:
        appearance_count = retrieve_appearances_by_host(host["slug"])
        first_most_recent = retrieve_first_most_recent_appearances(host["slug"])
        info = {}
        info["slug"] = host["slug"]
        info["name"] = host["name"]
        info["regular_shows"] = appearance_count["regular"]
        info["all_shows"] = appearance_count["all"]
        info["first"] = first_most_recent["first"]
        info["first_all"] = first_most_recent["first_all"]
        info["most_recent"] = first_most_recent["most_recent"]
        info["most_recent_all"] = first_most_recent["most_recent_all"]
        hosts_summary[host["slug"]] = info

    return hosts_summary
