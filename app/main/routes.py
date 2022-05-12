# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""Main Routes for Wait Wait Reports"""
from os.path import exists, join
from flask import Blueprint, Response, current_app, render_template, send_file

blueprint = Blueprint("main", __name__)


@blueprint.route("/")
def index():
    """View: Site Index Page"""
    return render_template("pages/index.html")


@blueprint.route("/robots.txt")
def robots_txt():
    """View: robots.txt File"""
    if not exists(join(current_app.root_path, "static", "robots.txt")):
        response = render_template("robots.txt")
        return Response(response, mimetype="text/plain")
    else:
        return send_file(
            join(current_app.root_path, "static", "robots.txt"), mimetype="text/plain"
        )
