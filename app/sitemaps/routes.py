# Copyright (c) 2018-2026 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Sitemap Routes for Wait Wait Reports."""

from flask import Blueprint, Response, current_app, redirect, render_template

blueprint = Blueprint("sitemaps", __name__)


@blueprint.route("/sitemap.xml")
def primary() -> Response:
    """View: Primary Sitemap XML."""
    sitemap: str = render_template("sitemaps/sitemap.xml")
    return Response(sitemap, mimetype="text/xml")


@blueprint.route("/sitemap-guests.xml")
def guests() -> Response:
    """View: Guests Sitemap XML."""
    sitemap: str = render_template("sitemaps/guests.xml")
    return Response(sitemap, mimetype="text/xml")


@blueprint.route("/sitemap-hosts.xml")
def hosts() -> Response:
    """View: Hosts Sitemap XML."""
    sitemap: str = render_template("sitemaps/hosts.xml")
    return Response(sitemap, mimetype="text/xml")


@blueprint.route("/sitemap-locations.xml")
def locations() -> Response:
    """View: Locations Sitemap XML."""
    sitemap: str = render_template("sitemaps/locations.xml")
    return Response(sitemap, mimetype="text/xml")


@blueprint.route("/sitemap-main.xml")
def main() -> Response:
    """View: Locations Sitemap XML."""
    sitemap: str = render_template("sitemaps/main.xml")
    return Response(sitemap, mimetype="text/xml")


@blueprint.route("/sitemap-on-this-day.xml")
def on_this_day() -> Response | None:
    if current_app.config["app_settings"]["enable_on_this_day_report"]:
        sitemap: str = render_template("sitemaps/on-this-day.xml")
        return Response(sitemap, mimetype="text/xml")
    else:
        return Response(None)


@blueprint.route("/sitemap-panelists.xml")
def panelists() -> Response:
    """View: Panelists Sitemap XML."""
    sitemap: str = render_template("sitemaps/panelists.xml")
    return Response(sitemap, mimetype="text/xml")


@blueprint.route("/sitemap-scorekeepers.xml")
def scorekeepers() -> Response:
    """View: Scorekeepers Sitemap XML."""
    sitemap: str = render_template("sitemaps/scorekeepers.xml")
    return Response(sitemap, mimetype="text/xml")


@blueprint.route("/sitemap-shows.xml")
def shows() -> Response:
    """View: Shows Sitemap XML."""
    sitemap: str = render_template(
        "sitemaps/shows.xml",
    )
    return Response(sitemap, mimetype="text/xml")
