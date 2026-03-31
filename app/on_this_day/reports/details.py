# Copyright (c) 2018-2026 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""On This Day Details module for Wait Wait Reports."""

from decimal import Decimal
from typing import Any

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection

from .debuts import (
    retrieve_host_debuts_by_month_day,
    retrieve_panelist_debuts_by_month_day,
    retrieve_scorekeeper_debuts_by_month_day,
)
from .scoring_exceptions import retrieve_scoring_exceptions_by_month_day
from .shows import retrieve_shows_by_month_day


def retrieve_details(
    month: int, day: int, database_connection: MySQLConnection | PooledMySQLConnection
) -> dict[str, list[dict[str, Any]]]:
    """Retrieve details for On This Day reports."""
    _host_debuts: list[dict[str, str | bool]] | None = (
        retrieve_host_debuts_by_month_day(
            month=month, day=day, database_connection=database_connection
        )
    )
    _panelist_debuts: list[dict[str, str | int | bool | Decimal]] | None = (
        retrieve_panelist_debuts_by_month_day(
            month=month, day=day, database_connection=database_connection
        )
    )
    _scorekeeper_debuts: list[dict[str, str | bool]] | None = (
        retrieve_scorekeeper_debuts_by_month_day(
            month=month, day=day, database_connection=database_connection
        )
    )
    _shows_details: list[dict[str, str | int | bool | Decimal]] | None = (
        retrieve_shows_by_month_day(
            month=month, day=day, database_connection=database_connection
        )
    )
    _guest_scoring_exceptions: list[dict[str, str | int | bool]] | None = (
        retrieve_scoring_exceptions_by_month_day(
            month=month, day=day, database_connection=database_connection
        )
    )

    return {
        "debuts": {
            "hosts": _host_debuts,
            "panelists": _panelist_debuts,
            "scorekeepers": _scorekeeper_debuts,
        },
        "guest_scoring_exceptions": _guest_scoring_exceptions,
        "shows": _shows_details,
    }
