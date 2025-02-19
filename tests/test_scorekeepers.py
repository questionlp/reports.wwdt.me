# Copyright (c) 2018-2025 Linh Pham
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
    assert b"Scorekeepers" in response.data
    assert b"Appearance Summary" in response.data


def test_appearance_summary(client: FlaskClient) -> None:
    """Testing scorekeepers.routes.appearance_summary."""
    response: TestResponse = client.get("/scorekeepers/appearance-summary")
    assert response.status_code == 200
    assert b"" in response.data
    assert b"" in response.data


def test_appearances_by_year(client: FlaskClient) -> None:
    """Testing scorekeepers.routes.appearances_by_year."""
    response: TestResponse = client.get("/scorekeepers/appearances-by-year")
    assert response.status_code == 200
    assert b"Appearances by Year" in response.data
    assert b"Regular Shows" in response.data
    assert b"All Shows" in response.data


def test_appearances_by_year_grid(client: FlaskClient) -> None:
    """Testing scorekeepers.routes.appearances_by_year_grid."""
    response: TestResponse = client.get("/scorekeepers/appearances-by-year/grid")
    assert response.status_code == 200
    assert b"Appearances by Year: Grid" in response.data
    assert b"Total" in response.data


def test_debuts_by_year(client: FlaskClient) -> None:
    """Testing scorekeepers.routes.debuts_by_year."""
    response: TestResponse = client.get("/scorekeepers/debuts-by-year")
    assert response.status_code == 200
    assert b"Debuts by Year" in response.data
    assert b"Scorekeeper debuts" in response.data
    assert b"# of Regular Appearances" in response.data


def test_scorekeeper_introductions(client: FlaskClient) -> None:
    """Testing scorekeepers.routes.scorekeeper_introductions."""
    response: TestResponse = client.get("/scorekeepers/scorekeeper-introductions")
    assert response.status_code == 200
    assert b"" in response.data
    assert b"" in response.data
