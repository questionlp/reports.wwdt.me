# Copyright (c) 2018-2024 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing Panelists Module and Blueprint Views."""
import pytest
from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_index(client: FlaskClient) -> None:
    """Testing panelists.routes.index."""
    response: TestResponse = client.get("/panelists/")
    assert response.status_code == 200
    assert b"Panelists" in response.data
    assert b"Aggregate Scores" in response.data
    assert b"Debuts by Year" in response.data


def test_aggregate_scores(client: FlaskClient) -> None:
    """Testing panelists.routes.aggregate_scores."""
    response: TestResponse = client.get("/panelists/aggregate-scores")
    assert response.status_code == 200
    assert b"Aggregate Score Statistics" in response.data
    assert b"Aggregate Score Spread" in response.data


def test_average_scores_by_year(client) -> None:
    """Testing panelists.routes.average_scores_by_year (GET)."""
    response: TestResponse = client.get("/panelists/average-scores-by-year")
    assert response.status_code == 200
    assert b"Average Scores by Year" in response.data
    assert b"Select a Panelist" in response.data


@pytest.mark.parametrize("panelist_slug", ["faith-salie"])
def test_average_scores_by_year_post(client: FlaskClient, panelist_slug: str) -> None:
    """Testing panelists.routes.average_scores_by_year (POST)."""
    response: TestResponse = client.post(
        "/panelists/average-scores-by-year", data={"panelist": panelist_slug}
    )
    assert response.status_code == 200
    assert b"Average Scores by Year" in response.data
    assert panelist_slug.encode("utf-8") in response.data
    assert b"stats float" in response.data


def test_average_scores_by_year_all(client: FlaskClient) -> None:
    """Testing panelists.routes.all_average_scores_by_year_all."""
    response: TestResponse = client.get("/panelists/average-scores-by-year-all")
    assert response.status_code == 200
    assert b"Average Scores by Year: All" in response.data
    assert b"stats float" in response.data
    assert b"No data available" not in response.data


def test_appearances_by_year(client: FlaskClient) -> None:
    """Testing panelists.routes.appearances_by_year."""
    response: TestResponse = client.get("/panelists/appearances-by-year")
    assert response.status_code == 200
    assert b"Appearances by Year" in response.data
    assert b"Total" in response.data
    assert b"No data available" not in response.data


def test_bluff_the_listener_statistics(client: FlaskClient) -> None:
    """Testing panelists.routes.bluff_the_listener_statistics."""
    response: TestResponse = client.get("/panelists/bluff-the-listener-statistics")
    assert response.status_code == 200
    assert b"Bluff the Listener Statistics" in response.data
    assert b"Unique Best Of" in response.data


def test_bluff_the_listener_statistics_by_year(client: FlaskClient) -> None:
    """Testing panelists.routes.bluff_the_listener_statistics_by_year."""
    response: TestResponse = client.get(
        "/panelists/bluff-the-listener-statistics-by-year"
    )
    assert response.status_code == 200
    assert b"Bluff the Listener Statistics by Year" in response.data
    assert b"Panelist" in response.data


@pytest.mark.parametrize("panelist_slug", ["roxanne-roberts"])
def test_bluff_the_listener_statistics_by_year_post(
    client: FlaskClient, panelist_slug: str
) -> None:
    """Testing panelists.routes.bluff_the_listener_statistics_by_year (POST)."""
    response: TestResponse = client.post(
        "/panelists/bluff-the-listener-statistics-by-year",
        data={"panelist": panelist_slug},
    )
    assert response.status_code == 200
    assert b"Bluff the Listener Statistics by Year" in response.data
    assert b"Panelist" in response.data
    assert b"Unique Best Of" in response.data


def test_debuts_by_year(client: FlaskClient) -> None:
    """Testing panelists.routes.debuts_by_year."""
    response: TestResponse = client.get("/panelists/debuts-by-year")
    assert response.status_code == 200
    assert b"Debuts by Year" in response.data
    assert b"# of Regular Appearances" in response.data


def test_first_appearance_wins(client: FlaskClient) -> None:
    """Testing panelists.first_appearance_wins."""
    response: TestResponse = client.get("/panelists/first-appearance-wins")
    assert response.status_code == 200
    assert b"First Appearance Win" in response.data
    assert b"Show Date" in response.data


def test_first_most_recent_appearances(client: FlaskClient) -> None:
    """Testing panelists.routes.first_most_recent_appearances."""
    response: TestResponse = client.get("/panelists/first-most-recent-appearances")
    assert response.status_code == 200
    assert b"First and Most Recent Appearances" in response.data
    assert b"Regular Shows" in response.data
    assert b"All Shows" in response.data


def test_losing_streaks(client: FlaskClient) -> None:
    """Testing panelists.routes.losing_streaks."""
    response: TestResponse = client.get("/panelists/losing-streaks")
    assert response.status_code == 200
    assert b"Losing Streaks" in response.data
    assert b"All Losses" in response.data
    assert b"Third Place Losses" in response.data


def test_panelist_vs_panelist(client) -> None:
    """Testing panelists.routes.panelist_vs_panelist (GET)."""
    response: TestResponse = client.get("/panelists/panelist-vs-panelist")
    assert response.status_code == 200
    assert b"Panelist vs Panelist" in response.data
    assert b"Select a Panelist" in response.data


@pytest.mark.parametrize("panelist_slug", ["faith-salie"])
def test_panelist_vs_panelist_post(client: FlaskClient, panelist_slug: str) -> None:
    """Testing panelists.routes.panelist_vs_panelist (POST)."""
    response: TestResponse = client.post(
        "/panelists/panelist-vs-panelist", data={"panelist": panelist_slug}
    )
    assert response.status_code == 200
    assert b"Panelist vs Panelist" in response.data
    assert panelist_slug.encode("utf-8") in response.data
    assert b"Ranked vs" in response.data


def test_panelist_vs_panelist_all(client: FlaskClient) -> None:
    """Testing panelists.routes.panelist_vs_panelist_all."""
    response: TestResponse = client.get("/panelists/panelist-vs-panelist/all")
    assert response.status_code == 200
    assert b"Panelist vs Panelist: All" in response.data
    assert b"Ranked vs" in response.data
    assert b"Total" in response.data


def test_panelist_vs_panelist_scoring(client: FlaskClient) -> None:
    """Testing panelists.routes.panelist_vs_panelist_scoring (GET)."""
    response: TestResponse = client.get("/panelists/panelist-vs-panelist-scoring")
    assert response.status_code == 200
    assert b"Panelist vs Panelist Scoring" in response.data
    assert b"Panelist 1" in response.data
    assert b"Panelist 2" in response.data


@pytest.mark.parametrize("panelist_1, panelist_2", [("adam-felber", "faith-salie")])
def test_panelist_vs_panelist_scoring_post(
    client: FlaskClient, panelist_1: str, panelist_2: str
) -> None:
    """Testing panelists.routes.panelist_vs_panelist_scoring (POST)."""
    response: TestResponse = client.post(
        "/panelists/panelist-vs-panelist-scoring",
        data={
            "panelist_1": panelist_1,
            "panelist_2": panelist_2,
        },
    )
    assert response.status_code == 200
    assert b"Panelist vs Panelist Scoring" in response.data
    assert panelist_1.encode("utf-8") in response.data
    assert panelist_2.encode("utf-8") in response.data
    assert b"Score" in response.data
    assert b"Rank" in response.data


def test_perfect_score_counts(client: FlaskClient) -> None:
    """Testing panelists.routes.perfect_score_counts."""
    response: TestResponse = client.get("/panelists/perfect-score-counts")
    assert response.status_code == 200
    assert b"Perfect Scores Count"
    assert b"Total Score Count"


def test_rankings_summary(client: FlaskClient) -> None:
    """Testing panelists.routes.rankings_summary."""
    response: TestResponse = client.get("/panelists/rankings-summary")
    assert response.status_code == 200
    assert b"Rankings Summary" in response.data
    assert b"First" in response.data
    assert b"Second" in response.data


def test_single_appearance(client: FlaskClient) -> None:
    """Testing panelists.routes.single_appearance."""
    response: TestResponse = client.get("/panelists/single-appearance")
    assert response.status_code == 200
    assert b"Single Appearance" in response.data
    assert b"Show Date" in response.data


def test_statistics_by_gender(client: FlaskClient) -> None:
    """Testing panelists.routes.statistics_by_gender."""
    response: TestResponse = client.get("/panelists/statistics-by-gender")
    assert response.status_code == 200
    assert b"Statistics by Gender" in response.data
    assert b"Std Dev" in response.data


def test_statistics_summary(client: FlaskClient) -> None:
    """Testing panelists.routes.statistics_summary."""
    response: TestResponse = client.get("/panelists/statistics-summary")
    assert response.status_code == 200
    assert b"Statistics Summary" in response.data
    assert b"Std Dev" in response.data


def test_win_streaks(client: FlaskClient) -> None:
    """Testing panelists.routes.win_streaks."""
    response: TestResponse = client.get("/panelists/win-streaks")
    assert response.status_code == 200
    assert b"Win Streaks" in response.data
    assert b"Outright Wins" in response.data
    assert b"Wins with Draws" in response.data
