# Copyright (c) 2018-2026 Linh Pham
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
    assert "Panelists" in response.text
    assert "Aggregate Scores" in response.text
    assert "Debuts by Year" in response.text


def test_aggregate_scores(client: FlaskClient) -> None:
    """Testing panelists.routes.aggregate_scores."""
    response: TestResponse = client.get("/panelists/aggregate-scores")
    assert response.status_code == 200
    assert "Aggregate Score Statistics" in response.text
    assert "Aggregate Score Spread" in response.text


def test_average_scores_by_year(client) -> None:
    """Testing panelists.routes.average_scores_by_year (GET)."""
    response: TestResponse = client.get("/panelists/average-scores-by-year")
    assert response.status_code == 200
    assert "Average Scores by Year" in response.text
    assert "Select a Panelist" in response.text


@pytest.mark.parametrize("panelist_slug", ["faith-salie"])
def test_average_scores_by_year_post(client: FlaskClient, panelist_slug: str) -> None:
    """Testing panelists.routes.average_scores_by_year (POST)."""
    response: TestResponse = client.post(
        "/panelists/average-scores-by-year", data={"panelist": panelist_slug}
    )
    assert response.status_code == 200
    assert "Average Scores by Year" in response.text
    assert panelist_slug.encode("utf-8") in response.data
    assert "stats float" in response.text


def test_average_scores_by_year_all(client: FlaskClient) -> None:
    """Testing panelists.routes.all_average_scores_by_year_all."""
    response: TestResponse = client.get("/panelists/average-scores-by-year-all")
    assert response.status_code == 200
    assert "Average Scores by Year: All" in response.text
    assert "stats float" in response.text
    assert "No data available" not in response.text


def test_appearance_counts_by_year(client: FlaskClient) -> None:
    """Testing panelists.routes.appearance_counts_by_year."""
    response: TestResponse = client.get("/panelists/appearance-counts-by-year")
    assert response.status_code == 200
    assert "Appearance Counts by Year" in response.text
    assert "Regular Shows" in response.text
    assert "All Shows" in response.text
    assert "No data available" not in response.text


def test_appearance_counts_by_year_grid(client: FlaskClient) -> None:
    """Testing panelists.routes.appearance_counts_by_year_grid."""
    response: TestResponse = client.get("/panelists/appearance-counts-by-year/grid")
    assert response.status_code == 200
    assert "Appearance Counts by Year: Grid" in response.text
    assert "Total" in response.text
    assert "No data available" not in response.text


def test_appearances_by_year(client: FlaskClient) -> None:
    """Testing panelists.routes.appearances_by_year."""
    response: TestResponse = client.get("/panelists/appearances-by-year")
    assert response.status_code == 200
    assert "Appearances by Year" in response.text
    assert "Select a Panelist" in response.text


@pytest.mark.parametrize("panelist_slug", ["faith-salie", "paula-poundstone"])
def test_appearances_by_year_post(
    client: FlaskClient,
    panelist_slug: str,
) -> None:
    """Testing panelists.routes.average_scores_by_year (POST)."""
    response: TestResponse = client.post(
        "/panelists/appearances-by-year", data={"panelist": panelist_slug}
    )
    assert response.status_code == 200
    assert "Appearances by Year" in response.text
    assert panelist_slug.encode("utf-8") in response.data
    assert "Repeat Of" in response.text


def test_bluff_the_listener_statistics(client: FlaskClient) -> None:
    """Testing panelists.routes.bluff_the_listener_statistics."""
    response: TestResponse = client.get("/panelists/bluff-the-listener-statistics")
    assert response.status_code == 200
    assert "Bluff the Listener Statistics" in response.text
    assert "Unique Best Of" in response.text


def test_bluff_the_listener_panelist_statistics_by_year(client: FlaskClient) -> None:
    """Testing panelists.routes.bluff_the_listener_panelist_statistics_by_year."""
    response: TestResponse = client.get(
        "/panelists/bluff-the-listener-panelist-statistics-by-year"
    )
    assert response.status_code == 200
    assert "Bluff the Listener Panelist Statistics by Year" in response.text
    assert "Panelist" in response.text


@pytest.mark.parametrize("panelist_slug", ["roxanne-roberts"])
def test_bluff_the_listener_panelist_statistics_by_year_post(
    client: FlaskClient, panelist_slug: str
) -> None:
    """Testing panelists.routes.bluff_the_listener_panelist_statistics_by_year (POST)."""
    response: TestResponse = client.post(
        "/panelists/bluff-the-listener-panelist-statistics-by-year",
        data={"panelist": panelist_slug},
    )
    assert response.status_code == 200
    assert "Bluff the Listener Panelist Statistics by Year" in response.text
    assert "Panelist" in response.text
    assert "Unique Best Of" in response.text


def test_bluff_the_listener_statistics_by_year(client: FlaskClient) -> None:
    """Testing panelists.routes.bluff_the_listener_statistics_by_year."""
    response: TestResponse = client.get(
        "/panelists/bluff-the-listener-statistics-by-year"
    )
    assert response.status_code == 200
    assert "Bluff the Listener Statistics by Year" in response.text
    assert "Select a Year" in response.text


@pytest.mark.parametrize("year", [2018, 2024])
def test_bluff_the_listener_statistics_by_year_post(
    client: FlaskClient, year: int
) -> None:
    """Testing panelists.routes.bluff_the_listener_statistics_by_year (POST)."""
    response: TestResponse = client.post(
        "/panelists/bluff-the-listener-statistics-by-year",
        data={"year": year},
    )
    assert response.status_code == 200
    assert "Bluff the Listener Statistics by Year" in response.text
    assert "Regular Bluff Segments" in response.text
    assert "Unique Best Of Bluff Segments" in response.text


def test_debuts_by_year(client: FlaskClient) -> None:
    """Testing panelists.routes.debuts_by_year."""
    response: TestResponse = client.get("/panelists/debuts-by-year")
    assert response.status_code == 200
    assert "Debuts by Year" in response.text
    assert "# of Regular Appearances" in response.text


def test_first_appearance_all_correct(client: FlaskClient) -> None:
    """Testing panelists.first_appearance_all_correct."""
    response: TestResponse = client.get("/panelists/first-appearance-all-correct")
    assert response.status_code == 200
    assert "First Appearance Answering All Lightning Questions Correct" in response.text
    assert "Show Date" in response.text


def test_first_appearance_wins(client: FlaskClient) -> None:
    """Testing panelists.first_appearance_wins."""
    response: TestResponse = client.get("/panelists/first-appearance-wins")
    assert response.status_code == 200
    assert "First Appearance Win" in response.text
    assert "Show Date" in response.text


@pytest.mark.parametrize("sort", [None, "panelist", "date"])
def test_first_appearances(client: FlaskClient, sort: str | None) -> None:
    """Testing panelists.first_appearances."""
    response: TestResponse = client.get(
        "/panelists/first-appearances", query_string={"sort": sort}
    )
    assert response.status_code == 200
    assert "First Appearances" in response.text
    assert "Show Date" in response.text
    assert "Rank" in response.text


def test_first_most_recent_appearances(client: FlaskClient) -> None:
    """Testing panelists.routes.first_most_recent_appearances."""
    response: TestResponse = client.get("/panelists/first-most-recent-appearances")
    assert response.status_code == 200
    assert "First and Most Recent Appearances" in response.text
    assert "Regular Shows" in response.text
    assert "All Shows" in response.text


def test_first_wins(client: FlaskClient) -> None:
    """Testing panelists.routes.first_wins."""
    response: TestResponse = client.get("/panelists/first-wins")
    assert response.status_code == 200
    assert "First Wins" in response.text
    assert "Outright Win" in response.text
    assert "Overall Win" in response.text


def test_highest_average_correct_answers_by_year(client: FlaskClient) -> None:
    """Testing panelists.routes.highest_average_correct_answers_by_year."""
    response: TestResponse = client.get(
        "/panelists/highest-average-correct-answers-by-year"
    )
    assert response.status_code == 200
    assert "Highest Average Correct Answers by Year" in response.text
    assert "Select a Year" in response.text


@pytest.mark.parametrize(
    "year, exclude_single", [(1998, False), (1998, True), (2018, False), (2018, True)]
)
def test_highest_average_correct_answers_by_year_post(
    client: FlaskClient, year: int, exclude_single: bool
) -> None:
    """Testing panelists.routes.highest_average_correct_answers_by_year (POST)."""
    response: TestResponse = client.post(
        "/panelists/highest-average-correct-answers-by-year",
        data={"year": year, "exclude_single": exclude_single},
    )
    assert response.status_code == 200
    assert "Highest Average Correct Answers by Year" in response.text
    assert "Average Correct Answers" in response.text


def test_highest_average_scores_by_year(client: FlaskClient) -> None:
    """Testing panelists.routes.highest_average_scores_by_year."""
    response: TestResponse = client.get("/panelists/highest-average-scores-by-year")
    assert response.status_code == 200
    assert "Highest Average Scores by Year" in response.text
    assert "Select a Year" in response.text


@pytest.mark.parametrize(
    "year, exclude_single", [(1998, False), (1998, True), (2018, False), (2018, True)]
)
def test_highest_average_scres_by_year_post(
    client: FlaskClient, year: int, exclude_single: bool
) -> None:
    """Testing panelists.routes.highest_average_correct_answers_by_year (POST)."""
    response: TestResponse = client.post(
        "/panelists/highest-average-scores-by-year",
        data={"year": year, "exclude_single": exclude_single},
    )
    assert response.status_code == 200
    assert "Highest Average Scores by Year" in response.text
    assert "Average Score" in response.text


def test_lightning_statistics_summary(client: FlaskClient) -> None:
    """Testing panelists.routes.lightning_statistics_summary."""
    response: TestResponse = client.get("/panelists/lightning-statistics-summary")
    assert response.status_code == 200
    assert "Lightning Fill In The Blank Statistics Summary" in response.text
    assert "Appearances" in response.text
    assert "Correct" in response.text


def test_losing_streaks(client: FlaskClient) -> None:
    """Testing panelists.routes.losing_streaks."""
    response: TestResponse = client.get("/panelists/losing-streaks")
    assert response.status_code == 200
    assert "Losing Streaks" in response.text
    assert "All Losses" in response.text
    assert "Third Place Losses" in response.text


def test_most_chosen_bluff_the_listener_by_year(client: FlaskClient) -> None:
    """Testing panelists.routes.most_chosen_bluff_the_listener_by_year."""
    response: TestResponse = client.get(
        "/panelists/most-chosen-bluff-the-listener-by-year"
    )
    assert response.status_code == 200
    assert "Most Chosen Bluff the Listener Stories by Year" in response.text
    assert "Select a Year" in response.text


@pytest.mark.parametrize("year", [1998, 2018])
def test_most_chosen_bluff_the_listener_by_year_post(
    client: FlaskClient, year: int
) -> None:
    """Testing panelists.routes.most_chosen_bluff_the_listener_by_year (POST)."""
    response: TestResponse = client.post(
        "/panelists/most-chosen-bluff-the-listener-by-year",
        data={"year": year},
    )
    assert response.status_code == 200
    assert "Most Chosen Bluff the Listener Stories by Year" in response.text
    assert "Select a Year" in response.text
    assert "# of Chosen Stories" in response.text


def test_most_chosen_correct_bluff_the_listener_by_year(client: FlaskClient) -> None:
    """Testing panelists.routes.most_chosen_correct_bluff_the_listener_by_year."""
    response: TestResponse = client.get(
        "/panelists/most-chosen-correct-bluff-the-listener-by-year"
    )
    assert response.status_code == 200
    assert "Most Chosen Correct Bluff the Listener Stories by Year" in response.text
    assert "Select a Year" in response.text


@pytest.mark.parametrize("year", [1998, 2018])
def test_most_chosen_correct_bluff_the_listener_by_year_post(
    client: FlaskClient, year: int
) -> None:
    """Testing panelists.routes.most_chosen_correct_bluff_the_listener_by_year (POST)."""
    response: TestResponse = client.post(
        "/panelists/most-chosen-correct-bluff-the-listener-by-year",
        data={"year": year},
    )
    assert response.status_code == 200
    assert "Most Chosen Correct Bluff the Listener Stories by Year" in response.text
    assert "Select a Year" in response.text
    assert "# of Chosen Correct Stories" in response.text


def test_most_correct_bluff_the_listener_by_year(client: FlaskClient) -> None:
    """Testing panelists.routes.most_correct_bluff_the_listener_by_year."""
    response: TestResponse = client.get(
        "/panelists/most-correct-bluff-the-listener-by-year"
    )
    assert response.status_code == 200
    assert "Most Correct Bluff the Listener Stories by Year" in response.text
    assert "Select a Year" in response.text


@pytest.mark.parametrize("year", [1998, 2018])
def test_most_correct_bluff_the_listener_by_year_post(
    client: FlaskClient, year: int
) -> None:
    """Testing panelists.routes.most_correct_bluff_the_listener_by_year (POST)."""
    response: TestResponse = client.post(
        "/panelists/most-correct-bluff-the-listener-by-year",
        data={"year": year},
    )
    assert response.status_code == 200
    assert "Most Correct Bluff the Listener Stories by Year" in response.text
    assert "Select a Year" in response.text
    assert "# of Correct Stories" in response.text


def test_most_wins_by_year(client: FlaskClient) -> None:
    """Testing panelists.routes.most_wins_by_year."""
    response: TestResponse = client.get("/panelists/most-wins-by-year")
    assert response.status_code == 200
    assert "Most Wins by Year" in response.text
    assert "Select a Year" in response.text


@pytest.mark.parametrize("year", [1998, 2018])
def test_most_wins_by_year_post(client: FlaskClient, year: int) -> None:
    """Testing panelists.routes.most_wins_by_year (POST)."""
    response: TestResponse = client.post(
        "/panelists/most-wins-by-year",
        data={"year": year},
    )
    assert response.status_code == 200
    assert "Most Wins by Year" in response.text
    assert "Outright Wins" in response.text


def test_panelist_vs_panelist(client) -> None:
    """Testing panelists.routes.panelist_vs_panelist (GET)."""
    response: TestResponse = client.get("/panelists/panelist-vs-panelist")
    assert response.status_code == 200
    assert "Panelist vs Panelist" in response.text
    assert "Select a Panelist" in response.text


@pytest.mark.parametrize("panelist_slug", ["faith-salie"])
def test_panelist_vs_panelist_post(client: FlaskClient, panelist_slug: str) -> None:
    """Testing panelists.routes.panelist_vs_panelist (POST)."""
    response: TestResponse = client.post(
        "/panelists/panelist-vs-panelist", data={"panelist": panelist_slug}
    )
    assert response.status_code == 200
    assert "Panelist vs Panelist" in response.text
    assert panelist_slug.encode("utf-8") in response.data
    assert "Ranked vs" in response.text


def test_panelist_vs_panelist_all(client: FlaskClient) -> None:
    """Testing panelists.routes.panelist_vs_panelist_all."""
    response: TestResponse = client.get("/panelists/panelist-vs-panelist/all")
    assert response.status_code == 200
    assert "Panelist vs Panelist: All" in response.text
    assert "Ranked vs" in response.text
    assert "Total" in response.text


def test_panelist_vs_panelist_scoring(client: FlaskClient) -> None:
    """Testing panelists.routes.panelist_vs_panelist_scoring (GET)."""
    response: TestResponse = client.get("/panelists/panelist-vs-panelist-scoring")
    assert response.status_code == 200
    assert "Panelist vs Panelist Scoring" in response.text
    assert "Panelist 1" in response.text
    assert "Panelist 2" in response.text


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
    assert "Panelist vs Panelist Scoring" in response.text
    assert panelist_1.encode("utf-8") in response.data
    assert panelist_2.encode("utf-8") in response.data
    assert "Score" in response.text
    assert "Rank" in response.text


def test_perfect_score_counts(client: FlaskClient) -> None:
    """Testing panelists.routes.perfect_score_counts."""
    response: TestResponse = client.get("/panelists/perfect-score-counts")
    assert response.status_code == 200
    assert "Perfect Scores Count"
    assert "Total Score Count"


def test_rankings_summary(client: FlaskClient) -> None:
    """Testing panelists.routes.rankings_summary."""
    response: TestResponse = client.get("/panelists/rankings-summary")
    assert response.status_code == 200
    assert "Rankings Summary" in response.text
    assert "First" in response.text
    assert "Second" in response.text


@pytest.mark.parametrize("sort", [None, "panelist", "date"])
def test_scoring_exceptions(client: FlaskClient, sort: str | None) -> None:
    """Testing panelists.first_appearances."""
    response: TestResponse = client.get(
        "/panelists/scoring-exceptions", query_string={"sort": sort}
    )
    assert response.status_code == 200
    assert "Scoring Exceptions and Anomalies" in response.text
    assert "Show Date" in response.text
    assert "Notes" in response.text


def test_single_appearance(client: FlaskClient) -> None:
    """Testing panelists.routes.single_appearance."""
    response: TestResponse = client.get("/panelists/single-appearance")
    assert response.status_code == 200
    assert "Single Appearance" in response.text
    assert "Show Date" in response.text


def test_statistics_by_gender(client: FlaskClient) -> None:
    """Testing panelists.routes.statistics_by_gender."""
    response: TestResponse = client.get("/panelists/statistics-by-gender")
    assert response.status_code == 200
    assert "Statistics by Gender" in response.text
    assert "Std Dev" in response.text


def test_statistics_summary(client: FlaskClient) -> None:
    """Testing panelists.routes.statistics_summary."""
    response: TestResponse = client.get("/panelists/statistics-summary")
    assert response.status_code == 200
    assert "Statistics Summary" in response.text
    assert "Std Dev" in response.text


def test_statistics_summary_by_year(client: FlaskClient) -> None:
    """Testing panelists.routes.statistics_summary_by_year."""
    response: TestResponse = client.get("/panelists/statistics-summary-by-year")
    assert response.status_code == 200
    assert "Statistics Summary by Year" in response.text
    assert "Select a Panelist" in response.text


@pytest.mark.parametrize("panelist_slug", ["roxanne-roberts"])
def test_statistics_summary_by_year_post(
    client: FlaskClient, panelist_slug: str
) -> None:
    """Testing panelists.statistics_summary_by_year (POST)."""
    response: TestResponse = client.post(
        "/panelists/statistics-summary-by-year",
        data={"panelist": panelist_slug},
    )
    assert response.status_code == 200
    assert "Statistics Summary by Year" in response.text
    assert "Panelist" in response.text
    assert "Appearances" in response.text
    assert "With Scores" in response.text


def test_win_streaks(client: FlaskClient) -> None:
    """Testing panelists.routes.win_streaks."""
    response: TestResponse = client.get("/panelists/win-streaks")
    assert response.status_code == 200
    assert "Win Streaks" in response.text
    assert "Outright Wins" in response.text
    assert "Wins with Draws" in response.text


def test_wins_draws_losses(client: FlaskClient) -> None:
    """Testing panelists.routes.wins_draws_losses."""
    response: TestResponse = client.get("/panelists/wins-draws-losses")
    assert response.status_code == 200
    assert "Wins, Draws and Losses" in response.text
    assert "Sort Column" in response.text
    assert "<table" in response.text


@pytest.mark.parametrize(
    "minimum_total, sort_column, sort_descending",
    [(0, "", False), (0, "", True), (5, "panelist", False), (5, "panelist", True)],
)
def test_wins_draws_losses_post(
    client: FlaskClient, minimum_total: int, sort_column: str, sort_descending: bool
) -> None:
    """Testing panelists.routes.wins_draws_losses (POST)."""
    response: TestResponse = client.post(
        "/panelists/wins-draws-losses",
        data={
            "minimum_total": minimum_total,
            "sort_column": sort_column,
            "sort_descending": sort_descending,
        },
    )
    assert response.status_code == 200
    assert "Wins, Draws and Losses" in response.text
    assert "Sort Column" in response.text
    assert "<table" in response.text
