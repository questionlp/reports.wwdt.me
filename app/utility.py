# Copyright (c) 2018-2024 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Utility functions used by the Wait Wait Reports."""

import json
from datetime import datetime
from functools import cmp_to_key
from operator import itemgetter

import markdown
import pytz
from flask import current_app
from mysql.connector import DatabaseError, connect

_utc_timezone = pytz.timezone("UTC")


def format_umami_analytics(umami_analytics: dict = None) -> str:
    """Return formatted string for Umami Analytics."""
    if not umami_analytics:
        return None

    _enabled = bool(umami_analytics.get("_enabled", False))

    if not _enabled:
        return None

    url = umami_analytics.get("url")
    website_id = umami_analytics.get("data_website_id")
    auto_track = bool(umami_analytics.get("data_auto_track", True))
    host_url = umami_analytics.get("data_host_url")
    domains = umami_analytics.get("data_domains")

    if url and website_id:
        host_url_prop = f'data-host-url="{host_url}"' if host_url else ""
        auto_track_prop = f'data-auto-track="{str(auto_track).lower()}"'
        domains_prop = f'data-domains="{domains}"' if domains else ""

        props = " ".join([host_url_prop, auto_track_prop, domains_prop])
        return f'<script defer src="{url}" data-website-id="{website_id}" {props.strip()}></script>'

    return None


def cmp(object_a, object_b):
    """Replacement for built-in function cmp that was removed in Python 3.

    Compare the two objects a and b and return an integer according to
    the outcome. The return value is negative if a < b, zero if a == b
    and strictly positive if a > b.

    https://portingguide.readthedocs.io/en/latest/comparisons.html#the-cmp-function
    """
    return (object_a > object_b) - (object_a < object_b)


def multi_key_sort(items: list[dict], columns: list) -> list[dict]:
    """Sorts a list of dictionaries based on a list of one or more keys."""
    comparers = [
        (
            (itemgetter(col[1:].strip()), -1)
            if col.startswith("-")
            else (itemgetter(col.strip()), 1)
        )
        for col in columns
    ]

    def comparer(left, right):
        comparer_iter = (cmp(fn(left), fn(right)) * mult for fn, mult in comparers)
        return next((result for result in comparer_iter if result), 0)

    return sorted(items, key=cmp_to_key(comparer))


def current_year(time_zone: pytz.timezone = _utc_timezone):
    """Return the current year."""
    now = datetime.now(time_zone)
    return now.strftime("%Y")


def date_string_to_date(**kwargs) -> datetime | None:
    """Used to convert an ISO-style date string into a datetime object."""
    if "date_string" in kwargs and kwargs["date_string"]:
        try:
            date_object = datetime.strptime(kwargs["date_string"], "%Y-%m-%d")
        except ValueError:
            return None

        return date_object

    return None


def generate_date_time_stamp(time_zone: pytz.timezone = _utc_timezone):
    """Generate a current date/timestamp string."""
    now = datetime.now(time_zone)
    return now.strftime("%Y-%m-%d %H:%M:%S %Z")


def md_to_html(text: str):
    """Converts Markdown text into HTML."""
    return markdown.markdown(text, output_format="html")


def pretty_jsonify(data):
    """Returns a prettier JSON output for an object than Flask's default tojson filter."""
    return json.dumps(data, indent=2)


def redirect_url(url: str, status_code: int = 302):
    """Returns a redirect response for a given URL."""
    # Use a custom response class to force set response headers
    # and handle the redirect to prevent browsers from caching redirect
    response = current_app.response_class(
        response=None, status=status_code, mimetype="text/plain"
    )

    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = 0
    response.headers["Location"] = url
    return response


def time_zone_parser(time_zone: str) -> pytz.timezone:
    """Parses a time zone name into a pytz.timezone object.

    Returns pytz.timezone object and string if time_zone is valid.
    Otherwise, returns UTC if time zone is not a valid tz value.
    """
    try:
        time_zone_object = pytz.timezone(time_zone)
        time_zone_string = time_zone_object.zone
    except (pytz.UnknownTimeZoneError, AttributeError, ValueError):
        time_zone_object = pytz.timezone("UTC")
        time_zone_string = time_zone_object.zone

    return time_zone_object, time_zone_string


def panelist_decimal_score_exists(database_settings: dict) -> bool:
    """Returns if the panelistscore_decimal column exists in the Wait Wait Stats Database."""
    try:
        database_connection = connect(**database_settings)
        cursor = database_connection.cursor()
        query = "SHOW COLUMNS FROM ww_showpnlmap WHERE Field = 'panelistscore_decimal'"
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()

        return bool(result)
    except DatabaseError:
        return False
