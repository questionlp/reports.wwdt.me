# Copyright (c) 2018-2026 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Utility functions used by the Wait Wait Reports."""

import json
import re
from datetime import datetime
from functools import cmp_to_key
from operator import itemgetter

import markdown
import pytz
from flask import current_app
from mysql.connector import DatabaseError, connect

_utc_timezone = pytz.timezone("UTC")


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


def generate_date_time_stamp(time_zone: pytz.timezone = _utc_timezone):
    """Generate a current date/timestamp string."""
    now = datetime.now(time_zone)
    return now.strftime("%Y-%m-%d %H:%M:%S %Z")


def md_to_html(markdown_text: str):
    """Converts Markdown text into HTML."""
    html_text = markdown.markdown(markdown_text, output_format="html")
    site_url = current_app.jinja_env.globals["site_url"]

    if html_text and site_url:
        pattern = r'(<a\s+href="((?:(?!' + site_url + r').)*?)")>([^<]+)</a>'
        replacement = r'\1 target="_blank">\3<i class="bi bi-box-arrow-up-right px-1" aria-hidden="true"></i></a>'
        updated_html = re.sub(pattern, replacement, html_text, flags=re.DOTALL)

    return updated_html


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
