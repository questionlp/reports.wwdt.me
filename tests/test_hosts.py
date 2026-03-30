# Copyright (c) 2018-2026 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing Hosts Module and Blueprint Views."""

import pytest
from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_index(client: FlaskClient) -> None:
    """Testing hosts.routes.index."""
    response: TestResponse = client.get("/hosts/")
    assert response.status_code == 200
    assert "Hosts" in response.text
    assert "Appearance Summary" in response.text


def test_appearance_summary(client: FlaskClient) -> None:
    """Testing hosts.routes.appearance_summary."""
    response: TestResponse = client.get("/hosts/appearance-summary")
    assert response.status_code == 200
    assert "Appearance Summary" in response.text
    assert "Regular Shows" in response.text
    assert "All Shows" in response.text


def test_appearance_counts_by_year(client: FlaskClient) -> None:
    """Testing hosts.routes.appearance_counts_by_year."""
    response: TestResponse = client.get("/hosts/appearance-counts-by-year")
    assert response.status_code == 200
    assert "Appearance Counts by Year" in response.text
    assert "Regular Shows" in response.text
    assert "All Shows" in response.text


def test_appearance_counts_by_year_grid(client: FlaskClient) -> None:
    """Testing hosts.routes.appearance_counts_by_year_grid."""
    response: TestResponse = client.get("/hosts/appearance-counts-by-year/grid")
    assert response.status_code == 200
    assert "Appearance Counts by Year: Grid" in response.text
    assert "Total" in response.text


def test_appearances_by_year(client: FlaskClient) -> None:
    """Testing hosts.routes.appearances_by_year."""
    response: TestResponse = client.get("/hosts/appearances-by-year")
    assert response.status_code == 200
    assert "Appearances by Year" in response.text
    assert "Select a Host" in response.text


@pytest.mark.parametrize("host_slug", ["peter-sagal", "luke-burbank"])
def test_appearances_by_year_post(client: FlaskClient, host_slug: str) -> None:
    """Testing hosts.routes.appearances_by_year (POST)."""
    response: TestResponse = client.post(
        "/hosts/appearances-by-year", data={"host": host_slug}
    )
    assert response.status_code == 200
    assert "Appearances by Year" in response.text
    assert host_slug.encode("utf-8") in response.data
    assert "Repeat Of" in response.text


def test_debuts_by_year(client: FlaskClient) -> None:
    """Testing hosts.routes.appearances_by_year_grid."""
    response: TestResponse = client.get("/hosts/debuts-by-year")
    assert response.status_code == 200
    assert "Debuts by Year" in response.text
    assert "# of Regular Appearances" in response.text


def test_guest_host_counts_by_year(client: FlaskClient) -> None:
    """Testing hosts.routes.guest_host_counts_by_year."""
    response: TestResponse = client.get("/hosts/guest-host-counts-by-year")
    assert response.status_code == 200
    assert "Guest Host Appearance Counts by Year" in response.text
    assert '<th scope="col">Year</th>' in response.text
