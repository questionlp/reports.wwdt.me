# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""Guests Redirect Routes for Wait Wait Reports"""
from flask import Blueprint, current_app, redirect, render_template, url_for
import mysql.connector

from app.utility import redirect_url

blueprint = Blueprint("guest_redirects", __name__)


@blueprint.route("/guest")
def index():
    """View: Guest Index"""
    return redirect_url(url_for("guests.index"))


@blueprint.route("/guest/best_of_only")
def best_of_only():
    """View: Guests Best Of Only Report Redirect"""
    return redirect_url(url_for("guests.best_of_only"))


@blueprint.route("/guest/most_appearances")
def most_appearances():
    """View: Guests Most Appearances Report"""
    return redirect_url(url_for("guests.most_appearances"))


@blueprint.route("/guest/scoring_exceptions")
def scoring_exceptions():
    """View: Guests Scoring Exceptions Report"""
    return redirect_url(url_for("guests.scoring_exceptions"))


@blueprint.route("/guest/three_pointers")
def three_pointers():
    """View: Guests Three Pointers Report"""
    return redirect_url(url_for("guests.three_pointers"))


# @blueprint.route("/<string:guest_slug>")
# def details(guest_slug: str):
#     """View: Guest Details"""
#     database_connection = mysql.connector.connect(**current_app.config["database"])
#     guest = Guest(database_connection=database_connection)
#     details = guest.retrieve_details_by_slug(guest_slug)
#     database_connection.close()

#     if not details:
#         return redirect(url_for("guests.index"))

#     guests = []
#     guests.append(details)
#     return render_template(
#         "guests/single.html", guest_name=details["name"], guests=guests
#     )


# @blueprint.route("/all")
# def all():
#     """View: Guest Details for All Guests"""
#     database_connection = mysql.connector.connect(**current_app.config["database"])
#     guest = Guest(database_connection=database_connection)
#     guests = guest.retrieve_all_details()
#     database_connection.close()

#     if not guests:
#         return redirect(url_for("guests.index"))

#     return render_template("guests/all.html", guests=guests)


# @blueprint.route("/random")
# def random():
#     """View: Random Guest Redirect"""
#     _slug = random_guest_slug()
#     return redirect_url(url_for("guests.details", guest_slug=_slug))
