# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""Guests Routes for Wait Wait Reports"""
from flask import Blueprint, render_template

from .reports.best_of_only import retrieve_best_of_only_guests
from .reports.most_appearances import guest_multiple_appearances
from .reports.scores import retrieve_all_scoring_exceptions, retrieve_all_three_pointers

blueprint = Blueprint("guests", __name__)


@blueprint.route("/")
def index():
    """View: Guests Index"""
    return render_template("guests/_index.html")


@blueprint.route("/best-of-only")
def best_of_only():
    """View: Guests Best Of Only Report"""
    _guests = retrieve_best_of_only_guests()
    return render_template("guests/best-of-only.html", guests=_guests)


@blueprint.route("/most-appearances")
def most_appearances():
    """View: Guests Most Appearances Report"""
    _guests = guest_multiple_appearances()
    return render_template("guests/most-appearances.html", guests=_guests)


@blueprint.route("/scoring-exceptions")
def scoring_exceptions():
    """View: Guests Scoring Exceptions Report"""
    _exceptions = retrieve_all_scoring_exceptions()
    return render_template("guests/scoring-exceptions.html", exceptions=_exceptions)


@blueprint.route("/three-pointers")
def three_pointers():
    """View: Guests Three Pointers Report"""
    _three_pointers = retrieve_all_three_pointers()
    return render_template("guests/three-pointers.html", three_pointers=_three_pointers)
