# Copyright (c) 2018-2023 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Main Routes for Wait Wait Reports."""
from os.path import exists, join
from pathlib import Path

from flask import Blueprint, Response, current_app, render_template, send_file

blueprint = Blueprint("main", __name__)


@blueprint.route("/")
def index():
    """View: Site Index Page."""
    return render_template("pages/_index.html")


@blueprint.route("/robots.txt")
def robots_txt():
    """View: robots.txt File."""
    static_robots = Path.cwd() / "app" / "static" / "robots.txt"
    if not static_robots.exists():
        response = render_template("robots.txt")
        return Response(response, mimetype="text/plain")
    else:
        return send_file(static_robots, mimetype="text/plain")
