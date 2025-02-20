# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing Hosts Module and Blueprint Views."""

from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_index(client: FlaskClient) -> None:
    """Testing hosts.routes.index."""
    response: TestResponse = client.get("/hosts/")
    assert response.status_code == 200
    assert b"Hosts" in response.data
    assert b"Appearance Summary" in response.data


def test_appearance_summary(client: FlaskClient) -> None:
    """Testing hosts.routes.appearance_summary."""
    response: TestResponse = client.get("/hosts/appearance-summary")
    assert response.status_code == 200
    assert b"Appearance Summary" in response.data
    assert b"Regular Shows" in response.data
    assert b"All Shows" in response.data


def test_appearance_counts_by_year(client: FlaskClient) -> None:
    """Testing hosts.routes.appearance_counts_by_year."""
    response: TestResponse = client.get("/hosts/appearance-counts-by-year")
    assert response.status_code == 200
    assert b"Appearance Counts by Year" in response.data
    assert b"Regular Shows" in response.data
    assert b"All Shows" in response.data


def test_appearance_counts_by_year_grid(client: FlaskClient) -> None:
    """Testing hosts.routes.appearance_counts_by_year_grid."""
    response: TestResponse = client.get("/hosts/appearance-counts-by-year/grid")
    assert response.status_code == 200
    assert b"Appearance Counts by Year: Grid" in response.data
    assert b"Total" in response.data


def test_debuts_by_year(client: FlaskClient) -> None:
    """Testing hosts.routes.appearances_by_year_grid."""
    response: TestResponse = client.get("/hosts/debuts-by-year")
    assert response.status_code == 200
    assert b"Debuts by Year" in response.data
    assert b"Host debuts" in response.data
    assert b"# of Regular Appearances" in response.data
