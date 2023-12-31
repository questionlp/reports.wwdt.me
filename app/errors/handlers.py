# Copyright (c) 2018-2023 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Error Handlers Module for Wait Wait Reports."""
from flask import render_template


def not_found(error):
    """Handle resource not found conditions."""
    return render_template("errors/404.html", error_description=error.description), 404


def handle_exception(error):
    """Handle exceptions in a slightly more graceful manner."""
    return render_template("errors/500.html"), 500
