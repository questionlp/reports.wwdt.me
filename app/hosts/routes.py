# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""Hosts Routes for Wait Wait Reports"""
from flask import Blueprint, render_template

from .reports.appearances import retrieve_appearance_summaries

blueprint = Blueprint("hosts", __name__)


@blueprint.route("/")
def index():
    """View: Hosts Index"""
    return render_template("hosts/index.html")


@blueprint.route("/appearance-summary")
def appearance_summary():
    """View: Hosts Appearance Summary Report"""
    summary = retrieve_appearance_summaries()
    return render_template("hosts/appearance-summary.html", summary=summary)
