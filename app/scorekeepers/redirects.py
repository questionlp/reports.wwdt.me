# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""Scorekeepers Redirect Routes for Wait Wait Reports"""
from flask import Blueprint, url_for

from app.utility import redirect_url

blueprint = Blueprint("scorekeepers_redirects", __name__)


@blueprint.route("/scorekeeper")
def index():
    """View: Scorekeepers Index Redirect"""
    return redirect_url(url_for("scorekeepers.index"), status_code=301)


@blueprint.route("/scorekeeper/appearance_summary")
def appearance_summary():
    """View: Scorekeepers Appearance Summary Report Redirect"""
    return redirect_url(url_for("scorekeepers.appearance_summary"), status_code=301)


@blueprint.route("/scorekeeper/introductions")
def introductions():
    """View: Scorekeepers Introductions Report Redirect"""
    return redirect_url(url_for("scorekeepers.introductions"), status_code=301)
