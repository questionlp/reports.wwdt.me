# Copyright (c) 2018-2026 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing On This Day Routes Module and Blueprint Views."""

import pytest
from flask import Flask
from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_index(app: Flask, client: FlaskClient) -> None:
    """Testing on_this_day.routes.index."""
    _report_enabled: bool = app.config["app_settings"]["enable_on_this_day_report"]
    response: TestResponse = client.get("/on-this-day")
    if _report_enabled:
        assert response.status_code == 200
        assert "omnibus report" in response.text
        assert "Host Debuts" in response.text
        assert "Panelist Debuts" in response.text
    else:
        assert response.status_code == 302


@pytest.mark.parametrize("month, day", [(1, 3), (9, 21)])
def test_month_day(app: Flask, client: FlaskClient, month: int, day: int) -> None:
    """Testing on_this_day.routes.month_day."""
    _report_enabled: bool = app.config["app_settings"]["enable_on_this_day_report"]
    response: TestResponse = client.get(f"/on-this-day/{month}/{day}")
    if _report_enabled:
        assert response.status_code == 200
        assert "omnibus report" in response.text
        assert "Host Debuts" in response.text
        assert "Panelist Debuts" in response.text
    else:
        assert response.status_code == 302


@pytest.mark.parametrize("month, day", [(13, 3), (9, 32)])
def test_month_day_invalid(
    app: Flask, client: FlaskClient, month: int, day: int
) -> None:
    """Testing on_this_day.routes.month_day."""
    _report_enabled: bool = app.config["app_settings"]["enable_on_this_day_report"]
    response: TestResponse = client.get(f"/on-this-day/{month}/{day}")
    if _report_enabled:
        assert response.status_code == 302
        assert "on-this-day" in response.location
    else:
        assert response.status_code == 302
