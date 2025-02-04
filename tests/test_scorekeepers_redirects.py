# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing Scorekeepers Redirects Module and Blueprint Views."""

from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_index(client: FlaskClient) -> None:
    """Testing scorekeepers.redirects.index."""
    response: TestResponse = client.get("/scorekeeper")
    assert response.status_code == 301
    assert response.location

    response: TestResponse = client.get("/scorekeepers")
    assert response.status_code == 301
    assert response.location


def test_appearance_summary(client: FlaskClient) -> None:
    """Testing scorekeepers.redirects.appearance_summary."""
    response: TestResponse = client.get("/scorekeeper/appearance_summary")
    assert response.status_code == 301
    assert response.location


def test_scorekeeper_introductions(client: FlaskClient) -> None:
    """Testing scorekeepers.redirects.scorekeeper_introductions."""
    response: TestResponse = client.get("/scorekeeper/introductions")
    assert response.status_code == 301
    assert response.location
