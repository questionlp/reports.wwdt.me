# Copyright (c) 2018-2023 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Sitemap Routes for Wait Wait Reports."""
from flask import Blueprint, Response, render_template

blueprint = Blueprint("sitemaps", __name__, template_folder="templates")


@blueprint.route("/sitemap.xml")
def primary():
    """View: Primary Sitemap XML."""
    sitemap = render_template("sitemaps/sitemap.xml")
    return Response(sitemap, mimetype="text/xml")


@blueprint.route("/sitemap-guests.xml")
def guests():
    """View: Guests Sitemap XML."""
    sitemap = render_template("sitemaps/guests.xml")
    return Response(sitemap, mimetype="text/xml")


@blueprint.route("/sitemap-hosts.xml")
def hosts():
    """View: Hosts Sitemap XML."""
    sitemap = render_template("sitemaps/hosts.xml")
    return Response(sitemap, mimetype="text/xml")


@blueprint.route("/sitemap-locations.xml")
def locations():
    """View: Locations Sitemap XML."""
    sitemap = render_template("sitemaps/locations.xml")
    return Response(sitemap, mimetype="text/xml")


@blueprint.route("/sitemap-panelists.xml")
def panelists():
    """View: Panelists Sitemap XML."""
    sitemap = render_template("sitemaps/panelists.xml")
    return Response(sitemap, mimetype="text/xml")


@blueprint.route("/sitemap-scorekeepers.xml")
def scorekeepers():
    """View: Scorekeepers Sitemap XML."""
    sitemap = render_template("sitemaps/scorekeepers.xml")
    return Response(sitemap, mimetype="text/xml")


@blueprint.route("/sitemap-shows.xml")
def shows():
    """View: Shows Sitemap XML."""
    sitemap = render_template("sitemaps/shows.xml")
    return Response(sitemap, mimetype="text/xml")
