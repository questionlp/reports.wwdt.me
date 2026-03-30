# Copyright (c) 2018-2026 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing Shows Module and Blueprint Views."""

import pytest
from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_index(client: FlaskClient) -> None:
    """Testing shows.routes.index."""
    response: TestResponse = client.get("/shows/")
    assert response.status_code == 200
    assert "Shows" in response.text
    assert "All Shows" in response.text
    assert "Original Shows" in response.text


def test_all_men_panel(client: FlaskClient) -> None:
    """Testing shows.routes.all_men_panel."""
    response: TestResponse = client.get("/shows/all-men-panel")
    assert response.status_code == 200
    assert "All Men Panel" in response.text
    assert "Guest" in response.text


@pytest.mark.parametrize("sort", [None, "asc", "desc"])
def test_all_shows(client: FlaskClient, sort: str | None) -> None:
    """Testing shows.routes.all_shows."""
    response: TestResponse = client.get("/shows/all-shows", query_string={"sort": sort})
    assert response.status_code == 200
    assert "All Shows" in response.text
    assert "Change sorting to" in response.text
    assert "Guest(s)" in response.text


def test_all_women_panel(client: FlaskClient) -> None:
    """Testing shows.routes.all_women_panel."""
    response: TestResponse = client.get("/shows/all-women-panel")
    assert response.status_code == 200
    assert "All Women Panel" in response.text
    assert "Guest" in response.text


@pytest.mark.parametrize("sort", [None, "asc", "desc"])
def test_best_of_shows(client: FlaskClient, sort: str | None) -> None:
    """Testing shows.routes.best_of_shows."""
    response: TestResponse = client.get(
        "/shows/best-of-shows", query_string={"sort": sort}
    )
    assert response.status_code == 200
    assert "Best Of Shows" in response.text
    assert "Change sorting to" in response.text
    assert "Guest(s)" in response.text


@pytest.mark.parametrize("sort", [None, "asc", "desc"])
def test_best_of_shows_with_guest_host(client: FlaskClient, sort: str | None) -> None:
    """Testing shows.routes.best_of_shows_with_guest_host."""
    response: TestResponse = client.get(
        "/shows/best-of-shows-with-guest-host", query_string={"sort": sort}
    )
    assert response.status_code == 200
    assert "Best Of Shows with a Guest Host" in response.text
    assert "Panelists" in response.text
    assert "Guest(s)" in response.text


@pytest.mark.parametrize("sort", [None, "asc", "desc"])
def test_best_of_shows_with_guest_host_scorekeeper(
    client: FlaskClient, sort: str | None
) -> None:
    """Testing shows.routes.best_of_shows_with_guest_host_scorekeeper."""
    response: TestResponse = client.get(
        "/shows/best-of-shows-with-guest-host-scorekeeper", query_string={"sort": sort}
    )
    assert response.status_code == 200
    assert "Best Of Shows with a Guest Host and a Guest Scorekeeper" in response.text
    assert "Panelists" in response.text
    assert "Guest(s)" in response.text


@pytest.mark.parametrize("sort", [None, "asc", "desc"])
def test_best_of_shows_with_guest_scorekeeper(
    client: FlaskClient, sort: str | None
) -> None:
    """Testing shows.routes.best_of_shows_with_guest_scorekeeper."""
    response: TestResponse = client.get(
        "/shows/best-of-shows-with-guest-scorekeeper", query_string={"sort": sort}
    )
    assert response.status_code == 200
    assert "Best Of Shows with a Guest Scorekeeper" in response.text
    assert "Panelists" in response.text
    assert "Guest(s)" in response.text


@pytest.mark.parametrize("sort", [None, "asc", "desc"])
def test_best_of_shows_with_unique_bluff(client: FlaskClient, sort: str | None) -> None:
    """Testing shows.routes.best_of_shows_with_unique_bluff."""
    response: TestResponse = client.get(
        "/shows/best-of-shows-with-unique-bluff-segments", query_string={"sort": sort}
    )
    assert response.status_code == 200
    assert "Best Of Shows with Unique Bluff the Listener Segments" in response.text
    assert "Change sorting to" in response.text
    assert "Bluff Segment #" in response.text


def test_high_scoring_shows(client: FlaskClient) -> None:
    """Testing shows.routes.high_scoring_shows."""
    response: TestResponse = client.get("/shows/high-scoring-shows")
    assert response.status_code == 200
    assert "High Scoring Shows" in response.text
    assert "Show Date" in response.text
    assert "Panelists" in response.text


def test_highest_score_equals_sum_other_scores(client: FlaskClient) -> None:
    """Testing shows.routes.highest_score_equals_sum_other_scores."""
    response: TestResponse = client.get("/shows/highest-score-equals-sum-other-scores")
    assert response.status_code == 200
    assert "Highest Score Equals the Sum of Other Scores" in response.text
    assert "Panelist" in response.text
    assert "Rank" in response.text


def test_lightning_round_answering_same_number_correct(client: FlaskClient) -> None:
    """Testing shows.routes.lightning_round_answering_same_number_correct."""
    response: TestResponse = client.get(
        "/shows/lightning-round-answering-same-number-correct"
    )
    assert response.status_code == 200
    assert (
        "Lightning Fill In The Blank: All Panelists Answering the Same Number of Questions Correct"
        in response.text
    )
    assert "Panelists" in response.text
    assert "Correct Answers" in response.text


def test_lightning_round_ending_three_way_tie(client: FlaskClient) -> None:
    """Testing shows.routes.lightning_round_ending_three_way_tie."""
    response: TestResponse = client.get("/shows/lightning-round-ending-three-way-tie")
    assert response.status_code == 200
    assert "Lightning Fill In The Blank Ending in a Three-Way Tie" in response.text
    assert "Panelists" in response.text
    assert "Final Score" in response.text


def test_lightning_round_starting_ending_three_way_tie(client: FlaskClient) -> None:
    """Testing shows.routes.lightning_round_starting_ending_three_way_tie."""
    response: TestResponse = client.get(
        "/shows/lightning-round-starting-ending-three-way-tie"
    )
    assert response.status_code == 200
    assert (
        "Lightning Fill In The Blank Starting and Ending in a Three-Way Tie"
        in response.text
    )
    assert "Panelists" in response.text
    assert "Final Score" in response.text


def test_lightning_round_starting_three_way_tie(client: FlaskClient) -> None:
    """Testing shows.routes.lightning_round_starting_three_way_tie."""
    response: TestResponse = client.get("/shows/lightning-round-starting-three-way-tie")
    assert response.status_code == 200
    assert "Lightning Fill In The Blank Starting in a Three-Way Tie" in response.text
    assert "Panelists" in response.text
    assert "Starting Score" in response.text


def test_lightning_round_starting_zero_points(client: FlaskClient) -> None:
    """Testing shows.routes.lightning_round_starting_zero_points."""
    response: TestResponse = client.get("/shows/lightning-round-starting-zero-points")
    assert response.status_code == 200
    assert "Lightning Fill In The Blank Starting with Zero Points" in response.text
    assert "Panelist" in response.text
    assert "Rank" in response.text


def test_lightning_round_zero_correct(client: FlaskClient) -> None:
    """Testing shows.routes.lightning_round_zero_correct."""
    response: TestResponse = client.get("/shows/lightning-round-zero-correct")
    assert response.status_code == 200
    assert (
        "Lightning Fill In The Blank Segment with Zero Correct Answers" in response.text
    )
    assert "Panelist" in response.text
    assert "Rank" in response.text


def test_low_scoring_shows(client: FlaskClient) -> None:
    """Testing shows.routes.low_scoring_shows."""
    response: TestResponse = client.get("/shows/low-scoring-shows")
    assert response.status_code == 200
    assert "Low Scoring Shows" in response.text
    assert "Show Date" in response.text
    assert "Panelists" in response.text


def testnot_my_job_guests_vs_bluff_the_listener_win_ratios(client: FlaskClient) -> None:
    """Testing shows.routes.not_my_job_vs_bluffs."""
    response: TestResponse = client.get(
        "/shows/not-my-job-guests-vs-bluff-the-listener-win-ratios"
    )
    assert response.status_code == 200
    assert "Not My Job Guests" in response.text
    assert "Bluff the Listener" in response.text
    assert "Win %" in response.text


@pytest.mark.parametrize("sort", [None, "asc", "desc"])
def test_original_shows(client: FlaskClient, sort: str | None) -> None:
    """Testing shows.routes.original_shows."""
    response: TestResponse = client.get(
        "/shows/original-shows", query_string={"sort": sort}
    )
    assert response.status_code == 200
    assert "Original Shows" in response.text
    assert "Panelists" in response.text
    assert "Guest" in response.text


def test_panel_gender_mix(client: FlaskClient) -> None:
    """Testing shows.routes.panel_gender_mix."""
    response: TestResponse = client.get("/shows/panel-gender-mix")
    assert response.status_code == 200
    assert "Panel Gender Mix" in response.text
    assert "3 W / 0 M" in response.text
    assert "Total" in response.text


@pytest.mark.parametrize("sort", [None, "asc", "desc"])
def test_repeat_best_of_shows(client: FlaskClient, sort: str | None) -> None:
    """Testing shows.routes.repeat_best_of_shows."""
    response: TestResponse = client.get(
        "/shows/repeat-best-of-shows", query_string={"sort": sort}
    )
    assert response.status_code == 200
    assert "Repeat Best Of Shows" in response.text
    assert "Change sorting to" in response.text
    assert "Guest(s)" in response.text


@pytest.mark.parametrize("sort", [None, "asc", "desc"])
def test_repeat_shows(client: FlaskClient, sort: str | None) -> None:
    """Testing shows.routes.repeat_shows."""
    response: TestResponse = client.get(
        "/shows/repeat-shows", query_string={"sort": sort}
    )
    assert response.status_code == 200
    assert "Repeat Shows" in response.text
    assert "Change sorting to" in response.text
    assert "Guest" in response.text


def test_search_shows_by_multiple_panelists(client: FlaskClient) -> None:
    """Testing shows.routes.search_shows_by_multiple_panelists (GET)."""
    response: TestResponse = client.get("/shows/search-shows-by-multiple-panelists")
    assert response.status_code == 200
    assert "Search Shows by Multiple Panelists" in response.text
    assert "Include Best Ofs" in response.text
    assert "Panelist 1" in response.text
    assert "Panelist 2" in response.text
    assert "Panelist 3" in response.text


@pytest.mark.parametrize("panelist_1", ["faith-salie"])
def test_search_shows_by_multiple_panelists_post_1(
    client: FlaskClient, panelist_1: str
) -> None:
    """Testing shows.routes.search_shows_by_multiple_panelists (POST) with 1panelist."""
    response: TestResponse = client.post(
        "/shows/search-shows-by-multiple-panelists",
        data={
            "panelist_1": panelist_1,
            "panelist_2": "",
            "panelist_3": "",
        },
    )
    assert response.status_code == 200
    assert "Search Shows by Multiple Panelists" in response.text
    assert "Include Best Ofs" in response.text
    assert "Best Of" in response.text
    assert "Repeat Of" in response.text
    assert "Location" in response.text


@pytest.mark.parametrize("panelist_1, panelist_2", [("faith-salie", "mo-rocca")])
def test_search_shows_by_multiple_panelists_post_2(
    client: FlaskClient, panelist_1: str, panelist_2: str
) -> None:
    """Testing shows.routes.search_shows_by_multiple_panelists (POST) with 2panelists."""
    response: TestResponse = client.post(
        "/shows/search-shows-by-multiple-panelists",
        data={
            "panelist_1": panelist_1,
            "panelist_2": panelist_2,
            "panelist_3": "",
        },
    )
    assert response.status_code == 200
    assert "Search Shows by Multiple Panelists" in response.text
    assert "Best Of" in response.text
    assert "Repeat Of" in response.text
    assert "Location" in response.text


@pytest.mark.parametrize(
    "panelist_1, panelist_2, panelist_3", [("faith-salie", "mo-rocca", "luke-burbank")]
)
def test_search_shows_by_multiple_panelists_post_3(
    client: FlaskClient, panelist_1: str, panelist_2: str, panelist_3: str
) -> None:
    """Testing shows.routes.search_shows_by_multiple_panelists (POST) with 3panelists."""
    response: TestResponse = client.post(
        "/shows/search-shows-by-multiple-panelists",
        data={
            "panelist_1": panelist_1,
            "panelist_2": panelist_2,
            "panelist_3": panelist_3,
        },
    )
    assert response.status_code == 200
    assert "Search Shows by Multiple Panelists" in response.text
    assert "Best Of" in response.text
    assert "Repeat Of" in response.text
    assert "Location" in response.text


@pytest.mark.parametrize(
    "panelist_1, panelist_2, panelist_3", [("faith-salie", "mo-rocca", "luke-burbank")]
)
def test_search_shows_by_multiple_panelists_post_3_best_of(
    client: FlaskClient, panelist_1: str, panelist_2: str, panelist_3: str
) -> None:
    """Testing shows.routes.search_shows_by_multiple_panelists (POST) with 3 panelists.

    Includes Best Of shows.
    """
    response: TestResponse = client.post(
        "/shows/search-shows-by-multiple-panelists",
        data={
            "panelist_1": panelist_1,
            "panelist_2": panelist_2,
            "panelist_3": panelist_3,
            "best_of": "on",
        },
    )
    assert response.status_code == 200
    assert "Search Shows by Multiple Panelists" in response.text
    assert "Best Of" in response.text
    assert "Repeat Of" in response.text
    assert "Location" in response.text


@pytest.mark.parametrize(
    "panelist_1, panelist_2, panelist_3", [("faith-salie", "mo-rocca", "luke-burbank")]
)
def test_search_shows_by_multiple_panelists_post_3_repeat(
    client: FlaskClient, panelist_1: str, panelist_2: str, panelist_3: str
) -> None:
    """Testing shows.routes.search_shows_by_multiple_panelists (POST) with 3 panelists.

    Includes repeat shows.
    """
    response: TestResponse = client.post(
        "/shows/search-shows-by-multiple-panelists",
        data={
            "panelist_1": panelist_1,
            "panelist_2": panelist_2,
            "panelist_3": panelist_3,
            "repeat": "on",
        },
    )
    assert response.status_code == 200
    assert "Search Shows by Multiple Panelists" in response.text
    assert "Best Of" in response.text
    assert "Repeat Of" in response.text
    assert "Location" in response.text


@pytest.mark.parametrize(
    "panelist_1, panelist_2, panelist_3", [("faith-salie", "mo-rocca", "luke-burbank")]
)
def test_search_shows_by_multiple_panelists_post_3_repeat_best_of(
    client: FlaskClient, panelist_1: str, panelist_2: str, panelist_3: str
) -> None:
    """Testing shows.routes.search_shows_by_multiple_panelists (POST) with 3 panelists.

    Includes Best Of and repeat shows.
    """
    response: TestResponse = client.post(
        "/shows/search-shows-by-multiple-panelists",
        data={
            "panelist_1": panelist_1,
            "panelist_2": panelist_2,
            "panelist_3": panelist_3,
            "repeat": "on",
        },
    )
    assert response.status_code == 200
    assert "Search Shows by Multiple Panelists" in response.text
    assert "Best Of" in response.text
    assert "Repeat Of" in response.text
    assert "Location" in response.text


def test_show_counts_by_year(client: FlaskClient) -> None:
    """Testing shows.routes.show_counts_by_year."""
    response: TestResponse = client.get("/shows/show-counts-by-year")
    assert response.status_code == 200
    assert "Show Counts by Year" in response.text
    assert "Best Of" in response.text
    assert "Repeat Best Ofs" in response.text


def test_show_descriptions(client: FlaskClient) -> None:
    """Testing shows.routes.show_descriptions."""
    response: TestResponse = client.get("/shows/show-descriptions")
    assert response.status_code == 200
    assert "Show Descriptions" in response.text
    assert "Show Date" in response.text


def test_show_notes(client: FlaskClient) -> None:
    """Testing shows.routes.show_notes."""
    response: TestResponse = client.get("/shows/show-notes")
    assert response.status_code == 200
    assert "Show Notes" in response.text
    assert "Show Date" in response.text


def test_shows_with_guest_host(client: FlaskClient) -> None:
    """Testing shows.routes.shows_with_guest_host."""
    response: TestResponse = client.get("/shows/shows-with-guest-host")
    assert response.status_code == 200
    assert "Shows with a Guest Host" in response.text
    assert "Panelists" in response.text
    assert "Guest(s)" in response.text


def test_shows_with_guest_host_scorekeeper(client: FlaskClient) -> None:
    """Testing shows.routes.shows_with_guest_host_scorekeeper."""
    response: TestResponse = client.get("/shows/shows-with-guest-host-scorekeeper")
    assert response.status_code == 200
    assert "Shows with a Guest Host and a Guest Scorekeeper" in response.text
    assert "Panelists" in response.text
    assert "Guest(s)" in response.text


def test_shows_with_guest_scorekeeper(client: FlaskClient) -> None:
    """Testing shows.routes.shows_with_guest_scorekeeper."""
    response: TestResponse = client.get("/shows/shows-with-guest-scorekeeper")
    assert response.status_code == 200
    assert "Shows with a Guest Scorekeeper" in response.text
    assert "Panelists" in response.text
    assert "Guest(s)" in response.text


def test_shows_with_panelists_matching_initials(client: FlaskClient) -> None:
    """Testing shows.routes.shows_with_panelists_matching_initials."""
    response: TestResponse = client.get("/shows/shows-with-panelists-matching-initials")
    assert response.status_code == 200
    assert "Shows with Panelists Having Matching Initials"
    assert "Show Date"
    assert "Location"


def test_shows_with_perfect_panelist_scores(client: FlaskClient) -> None:
    """Testing shows.routes.shows_with_perfect_panelist_scores."""
    response: TestResponse = client.get("/shows/shows-with-perfect-panelist-scores")
    assert response.status_code == 200
    assert "Shows with Perfect Panelist Scores"
    assert "Show Date"
