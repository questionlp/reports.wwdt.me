# Copyright (c) 2018-2026 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing Scorekeepers Module and Blueprint Views."""

import pytest
from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_index(client: FlaskClient) -> None:
    """Testing scorekeepers.routes.index."""
    response: TestResponse = client.get("/scorekeepers/")
    assert response.status_code == 200
    assert "Scorekeepers" in response.text
    assert "Appearance Summary" in response.text


def test_appearance_summary(client: FlaskClient) -> None:
    """Testing scorekeepers.routes.appearance_summary."""
    response: TestResponse = client.get("/scorekeepers/appearance-summary")
    assert response.status_code == 200
    assert "Regular Shows" in response.text
    assert "All Shows" in response.text


def test_appearance_counts_by_year(client: FlaskClient) -> None:
    """Testing scorekeepers.routes.appearance_counts_by_year."""
    response: TestResponse = client.get("/scorekeepers/appearance-counts-by-year")
    assert response.status_code == 200
    assert "Appearance Counts by Year" in response.text
    assert "Regular Shows" in response.text
    assert "All Shows" in response.text


def test_appearance_counts_by_year_grid(client: FlaskClient) -> None:
    """Testing scorekeepers.routes.appearance_counts_by_year_grid."""
    response: TestResponse = client.get("/scorekeepers/appearance-counts-by-year/grid")
    assert response.status_code == 200
    assert "Appearance Counts by Year: Grid" in response.text
    assert "Total" in response.text


def test_appearances_by_year(client: FlaskClient) -> None:
    """Testing scorekeepers.routes.appearances_by_year."""
    response: TestResponse = client.get("/scorekeepers/appearances-by-year")
    assert response.status_code == 200
    assert "Appearances by Year" in response.text
    assert "Select a Scorekeeper" in response.text


@pytest.mark.parametrize("scorekeeper_slug", ["carl-kasell", "bill-kurtis"])
def test_appearances_by_year_post(client: FlaskClient, scorekeeper_slug: str) -> None:
    """Testing scorekeepers.routes.average_scores_by_year (POST)."""
    response: TestResponse = client.post(
        "/scorekeepers/appearances-by-year",
        data={"scorekeeper": scorekeeper_slug},
    )
    assert response.status_code == 200
    assert "Appearances by Year" in response.text
    assert scorekeeper_slug.encode("utf-8") in response.data
    assert "Repeat Of" in response.text


def test_debuts_by_year(client: FlaskClient) -> None:
    """Testing scorekeepers.routes.debuts_by_year."""
    response: TestResponse = client.get("/scorekeepers/debuts-by-year")
    assert response.status_code == 200
    assert "Debuts by Year" in response.text
    assert "# of Regular Appearances" in response.text


def test_scorekeeper_introductions(client: FlaskClient) -> None:
    """Testing scorekeepers.routes.scorekeeper_introductions."""
    response: TestResponse = client.get("/scorekeepers/scorekeeper-introductions")
    assert response.status_code == 200
    assert "Show Date" in response.text
    assert "Best Of" in response.text


def test_guest_scorekeeper_counts_by_year(client: FlaskClient) -> None:
    """Testing scorekeepers.routes.guest_scorekeeper_counts_by_year."""
    response: TestResponse = client.get(
        "/scorekeepers/guest-scorekeeper-counts-by-year"
    )
    assert response.status_code == 200
    assert "Guest Scorekeeper Appearance Counts by Year" in response.text
    assert '<th scope="col">Year</th>' in response.text
