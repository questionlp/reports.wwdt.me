# Copyright (c) 2018-2025 Linh Pham
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


def test_bluff_the_listener_statistics(client: FlaskClient) -> None:
    """Testing panelists.redirects.bluff_the_listener_statistics."""
    response: TestResponse = client.get("/panelist/bluff_stats")
    assert response.status_code == 301
    assert response.location

    response: TestResponse = client.get("/panelists/bluff-stats")
    assert response.status_code == 301
    assert response.location


def test_bluff_the_listener_statistics_by_year(client: FlaskClient) -> None:
    """Testing panelists.redirects.bluff_the_listener_statistics_by_year."""
    response: TestResponse = client.get("/panelists/bluff-stats-by-year")
    assert response.status_code == 301
    assert response.location


def test_debuts_by_year(client: FlaskClient) -> None:
    """Testing panelists.redirects.debuts_by_year."""
    response: TestResponse = client.get("/panelist/debut_by_year")
    assert response.status_code == 301
    assert response.location

    response: TestResponse = client.get("/panelists/debut-by-year")
    assert response.status_code == 301
    assert response.location


def test_first_most_recent_appearances(client: FlaskClient) -> None:
    """Testing panelists.redirects.first_most_recent_appearances."""
    response: TestResponse = client.get("/panelist/first_most_recent_appearances")
    assert response.status_code == 301
    assert response.location


def test_statistics_by_gender(client: FlaskClient) -> None:
    """Testing panelists.redirects.statistics_by_gender."""
    response: TestResponse = client.get("/panelist/gender_stats")
    assert response.status_code == 301
    assert response.location

    response: TestResponse = client.get("/panelists/gender-stats")
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


def test_panelist_vs_panelist(client: FlaskClient) -> None:
    """Testing panelists.redirects.panelist_vs_panelist."""
    response: TestResponse = client.get("/panelist/panelist_pvp_report")
    assert response.status_code == 301
    assert response.location

    response: TestResponse = client.get("/panelist/panelist_vs_panelist")
    assert response.status_code == 301
    assert response.location

    response: TestResponse = client.get("/panelist/pvp")
    assert response.status_code == 301
    assert response.location

    response: TestResponse = client.get("/panelists/panelist-pvp")
    assert response.status_code == 301
    assert response.location


def test_panelist_vs_panelist_all(client: FlaskClient) -> None:
    """Testing panelists.redirects.panelist_vs_panelist_all."""
    response: TestResponse = client.get("/panelists/panelist-pvp/all")
    assert response.status_code == 301
    assert response.location


def test_panelist_vs_panelist_scoring(client: FlaskClient) -> None:
    """Testing panelists.redirects.panelist_vs_panelist_scoring."""
    response: TestResponse = client.get("/panelist/panelist_vs_panelist_scoring")
    assert response.status_code == 301
    assert response.location


def test_perfect_score_counts(client: FlaskClient) -> None:
    """Testing panelists.redirects.perfect_score_counts."""
    response: TestResponse = client.get("/panelists/perfect-scores")
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


def test_statistics_summary(client: FlaskClient) -> None:
    """Testing panelists.redirects.statistics_summary."""
    response: TestResponse = client.get("/panelist/stats_summary")
    assert response.status_code == 301
    assert response.location

    response: TestResponse = client.get("/panelist/statistics_summary")
    assert response.status_code == 301
    assert response.location

    response: TestResponse = client.get("/panelists/stats-summary")
    assert response.status_code == 301
    assert response.location


def test_win_streaks(client: FlaskClient) -> None:
    """Testing panelists.redirects.win_streaks."""
    response: TestResponse = client.get("/panelist/win_streaks")
    assert response.status_code == 301
    assert response.location
