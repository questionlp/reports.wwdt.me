# Copyright (c) 2018-2023 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing Panelists Redirects Module and Blueprint Views."""
from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_index(client: FlaskClient) -> None:
    """Testing panelists.redirects.index."""
    response: TestResponse = client.get("/panelist")
    assert response.status_code == 301
    assert response.location

    response: TestResponse = client.get("/panelists")
    assert response.status_code == 301
    assert response.location


def test_aggregate_scores(client: FlaskClient) -> None:
    """Testing panelists.redirects.aggregate_scores."""
    response: TestResponse = client.get("/panelist/aggregate_scores")
    assert response.status_code == 301
    assert response.location


def test_appearances_by_year(client: FlaskClient) -> None:
    """Testing panelists.redirects.appearances_by_year."""
    response: TestResponse = client.get("/panelist/appearances_by_year")
    assert response.status_code == 301
    assert response.location


def test_bluff_stats(client: FlaskClient) -> None:
    """Testing panelists.redirects.bluff_stats."""
    response: TestResponse = client.get("/panelist/bluff_stats")
    assert response.status_code == 301
    assert response.location


def test_debut_by_year(client: FlaskClient) -> None:
    """Testing panelists.redirects.debut_by_year."""
    response: TestResponse = client.get("/panelist/debut_by_year")
    assert response.status_code == 301
    assert response.location


def test_first_most_recent_appearances(client: FlaskClient) -> None:
    """Testing panelists.redirects.first_most_recent_appearances."""
    response: TestResponse = client.get("/panelist/first_most_recent_appearances")
    assert response.status_code == 301
    assert response.location


def test_gender_stats(client: FlaskClient) -> None:
    """Testing panelists.redirects.gender_stats."""
    response: TestResponse = client.get("/panelist/gender_stats")
    assert response.status_code == 301
    assert response.location


def test_losing_streaks(client: FlaskClient) -> None:
    """Testing panelists.redirects.losing_streaks."""
    response: TestResponse = client.get("/panelist/losing_streaks")
    assert response.status_code == 301
    assert response.location


def test_panel_gender_mix(client: FlaskClient) -> None:
    """Testing panelists.redirects.panel_gender_mix."""
    response: TestResponse = client.get("/panelist/panel_gender_mix")
    assert response.status_code == 301
    assert response.location

    response: TestResponse = client.get("/panelists/panel_gender_mix")
    assert response.status_code == 301
    assert response.location


def test_pvp(client: FlaskClient) -> None:
    """Testing panelists.redirects.pvp."""
    response: TestResponse = client.get("/panelist/panelist_pvp_report")
    assert response.status_code == 301
    assert response.location

    response: TestResponse = client.get("/panelist/panelist_vs_panelist")
    assert response.status_code == 301
    assert response.location

    response: TestResponse = client.get("/panelist/pvp")
    assert response.status_code == 301
    assert response.location


def test_panelist_vs_panelist_scoring(client: FlaskClient) -> None:
    """Testing panelists.redirects.panelist_vs_panelist_scoring."""
    response: TestResponse = client.get("/panelist/panelist_vs_panelist_scoring")
    assert response.status_code == 301
    assert response.location


def test_rankings_summary(client: FlaskClient) -> None:
    """Testing panelists.redirects.rankings_summary."""
    response: TestResponse = client.get("/panelist/rankings_summary")
    assert response.status_code == 301
    assert response.location


def test_single_appearance(client: FlaskClient) -> None:
    """Testing panelists.redirects.single_appearance."""
    response: TestResponse = client.get("/panelist/single_appearance")
    assert response.status_code == 301
    assert response.location


def test_stats_summary(client: FlaskClient) -> None:
    """Testing panelists.redirects.stats_summary."""
    response: TestResponse = client.get("/panelist/stats_summary")
    assert response.status_code == 301
    assert response.location


def test_win_streaks(client: FlaskClient) -> None:
    """Testing panelists.redirects.win_streaks."""
    response: TestResponse = client.get("/panelist/win_streaks")
    assert response.status_code == 301
    assert response.location
