# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""Main Redirect Routes for Wait Wait Reports"""
from datetime import datetime
from flask import Blueprint, url_for

from app.utility import date_string_to_date, redirect_url

blueprint = Blueprint("main_redirects", __name__)


@blueprint.route("/favicon.ico")
def favicon():
    """Redirect: /favicon.ico to /static/favicon.ico"""
    return redirect_url(url_for("static", filename="favicon.ico"))
