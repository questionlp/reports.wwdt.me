# Copyright (c) 2018-2024 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing Scorekeepers Module and Blueprint Views."""
from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_index(client: FlaskClient) -> None:
    """Testing scorekeepers.routes.index."""
    response: TestResponse = client.get("/scorekeepers/")
    assert response.status_code == 200
    assert b"Scorekeepers Reports" in response.data
    assert b"Appearance Summary" in response.data


def test_appearance_summary(client: FlaskClient) -> None:
    """Testing scorekeepers.routes.appearance_summary."""
    response: TestResponse = client.get("/scorekeepers/appearance-summary")
    assert response.status_code == 200
    assert b"" in response.data
    assert b"" in response.data


def test_introductions(client: FlaskClient) -> None:
    """Testing scorekeepers.routes.introductions."""
    response: TestResponse = client.get("/scorekeepers/introductions")
    assert response.status_code == 200
    assert b"" in response.data
    assert b"" in response.data
