# Copyright (c) 2018-2026 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing On This Day Routes Module and Blueprint Views."""

from flask import Flask
from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_index(app: Flask, client: FlaskClient):
    _report_enabled: bool = app.config["app_settings"].get(
        "enable_on_this_day_report", False
    )
    response: TestResponse = client.get("/on-this-day")
    if _report_enabled:
        assert response.status_code == 200
    else:
        assert response.status_code == 404
