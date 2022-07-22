# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""WWDTM Common Panelist Report Functions"""
from typing import Any, Dict, List

import mysql.connector


def retrieve_panelists(
    database_connection: mysql.connector.connect,
) -> List[Dict[str, Any]]:
    """Retrieves a list of all available panelists from the database"""

    if not database_connection.is_connected():
        database_connection.reconnect()

    cursor = database_connection.cursor(named_tuple=True)
    query = (
        "SELECT p.panelistid, p.panelist, p.panelistslug "
        "FROM ww_panelists p "
        "WHERE p.panelist <> '<Multiple>' "
        "ORDER BY p.panelistslug ASC;"
    )
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()

    if not result:
        return None

    _panelists = []
    for row in result:
        _panelists.append(
            {
                "id": row.panelistid,
                "slug": row.panelistslug,
                "name": row.panelist,
            }
        )

    return _panelists
