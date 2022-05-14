# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""Shows Routes for Wait Wait Reports"""
from typing import Optional

from flask import Blueprint, render_template

from .reports.panel_gender_mix import panel_gender_mix_breakdown

blueprint = Blueprint("shows", __name__)


@blueprint.route("/")
def index():
    """View: Shows Index"""
    return render_template("shows/_index.html")


@blueprint.route("/panel-gender-mix")
def panel_gender_mix(gender: Optional[str] = "female"):
    """View: Shows Panel Gender Mix Report"""
    gender_tag = gender[0].upper()
    mix = panel_gender_mix_breakdown(gender=gender)
    return render_template(
        "shows/panel-gender-mix.html", panel_gender_mix=mix, gender=gender_tag
    )
