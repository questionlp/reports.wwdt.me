# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2023 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""Utility functions used by the Wait Wait Reports"""

from datetime import datetime
from functools import cmp_to_key
import json
from typing import Dict, List

from dateutil import parser
from flask import current_app
import markdown
from mysql.connector import connect, DatabaseError
from operator import itemgetter
import pytz


def cmp(object_a, object_b):
    """Replacement for built-in function cmp that was removed in Python 3

    Compare the two objects a and b and return an integer according to
    the outcome. The return value is negative if a < b, zero if a == b
    and strictly positive if a > b.

    https://portingguide.readthedocs.io/en/latest/comparisons.html#the-cmp-function
    """

    return (object_a > object_b) - (object_a < object_b)


def multi_key_sort(items: List[Dict], columns: List) -> List[Dict]:
    """Sorts a list of dictionaries based on a list of one or more keys"""
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


def current_year(time_zone: pytz.timezone = pytz.timezone("UTC")):
    """Return the current year"""
    now = datetime.now(time_zone)
    return now.strftime("%Y")


def date_string_to_date(**kwargs):
    """Used to convert an ISO-style date string into a datetime object"""
    if "date_string" in kwargs and kwargs["date_string"]:
        try:
            date_object = parser.parse(kwargs["date_string"])
            return date_object

        except ValueError:
            return None

    return None


def generate_date_time_stamp(time_zone: pytz.timezone = pytz.timezone("UTC")):
    """Generate a current date/timestamp string"""
    now = datetime.now(time_zone)
    return now.strftime("%Y-%m-%d %H:%M:%S %Z")


def md_to_html(text: str):
    """Converts Markdown text into HTML"""
    return markdown.markdown(text, output_format="html")


def pretty_jsonify(data):
    """Returns a prettier JSON output for an object than Flask's default
    tojson filter"""
    return json.dumps(data, indent=2)


def redirect_url(url: str, status_code: int = 302):
    """Returns a redirect response for a given URL"""

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
    Otherwise, returns UTC if time zone is not a valid tz value."""

    try:
        time_zone_object = pytz.timezone(time_zone)
        time_zone_string = time_zone_object.zone
    except (pytz.UnknownTimeZoneError, AttributeError, ValueError):
        time_zone_object = pytz.timezone("UTC")
        time_zone_string = time_zone_object.zone

    return time_zone_object, time_zone_string


def panelist_decimal_score_exists(database_settings: Dict) -> bool:
    """Checks to see if the panelistscore_decimal column exists in the
    ww_showpnlmap table in the Wait Wait Stats Database and returns
    a bool reflecting the results"""

    try:
        database_connection = connect(**database_settings)
        cursor = database_connection.cursor()
        query = "SHOW COLUMNS FROM ww_showpnlmap WHERE Field = 'panelistscore_decimal'"
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        if result:
            return True
        else:
            return False
    except DatabaseError:
        return False
