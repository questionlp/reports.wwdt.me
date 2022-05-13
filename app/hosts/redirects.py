# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""Hosts Redirect Routes for Wait Wait Reports"""
from flask import Blueprint, url_for

from app.utility import redirect_url

blueprint = Blueprint("hosts_redirects", __name__)


@blueprint.route("/host")
def index():
    """View: Hosts Index Redirect"""
    return redirect_url(url_for("hosts.index"), status_code=301)


@blueprint.route("/host/appearance_summary")
def best_of_only():
    """View: Hosts Appearance Summary Report Redirect"""
    return redirect_url(url_for("hosts.appearance_summary"), status_code=301)
