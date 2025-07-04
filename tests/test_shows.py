# Copyright (c) 2018-2025 Linh Pham
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
    assert b"Shows" in response.data
    assert b"All Shows" in response.data
    assert b"Original Shows" in response.data


@pytest.mark.parametrize("sort", [None, "asc", "desc"])
def test_all_shows(client: FlaskClient, sort: str | None) -> None:
    """Testing shows.routes.all_shows."""
    response: TestResponse = client.get("/shows/all-shows", query_string={"sort": sort})
    assert response.status_code == 200
    assert b"All Shows" in response.data
    assert b"Change sorting to" in response.data
    assert b"Guest" in response.data


def test_all_women_panel(client: FlaskClient) -> None:
    """Testing shows.routes.all_women_panel."""
    response: TestResponse = client.get("/shows/all-women-panel")
    assert response.status_code == 200
    assert b"All Women Panel" in response.data
    assert b"Guest" in response.data


@pytest.mark.parametrize("sort", [None, "asc", "desc"])
def test_best_of_shows(client: FlaskClient, sort: str | None) -> None:
    """Testing shows.routes.best_of_shows."""
    response: TestResponse = client.get(
        "/shows/best-of-shows", query_string={"sort": sort}
    )
    assert response.status_code == 200
    assert b"Best Of Shows" in response.data
    assert b"Change sorting to" in response.data
    assert b"Guest" in response.data


def test_high_scoring_shows(client: FlaskClient) -> None:
    """Testing shows.routes.high_scoring_shows."""
    response: TestResponse = client.get("/shows/high-scoring-shows")
    assert response.status_code == 200
    assert b"High Scoring Shows" in response.data
    assert b"Show Date" in response.data
    assert b"Panelists" in response.data


def test_highest_score_equals_sum_other_scores(client: FlaskClient) -> None:
    """Testing shows.routes.highest_score_equals_sum_other_scores."""
    response: TestResponse = client.get("/shows/highest-score-equals-sum-other-scores")
    assert response.status_code == 200
    assert b"Highest Score Equals the Sum of Other Scores" in response.data
    assert b"Panelist" in response.data
    assert b"Rank" in response.data


def test_lightning_round_answering_same_number_correct(client: FlaskClient) -> None:
    """Testing shows.routes.lightning_round_answering_same_number_correct."""
    response: TestResponse = client.get(
        "/shows/lightning-round-answering-same-number-correct"
    )
    assert response.status_code == 200
    assert (
        b"Lightning Round All Panelists Answering the Same Number of Questions Correct"
        in response.data
    )
    assert b"Panelists" in response.data
    assert b"Correct Answers" in response.data


def test_lightning_round_ending_three_way_tie(client: FlaskClient) -> None:
    """Testing shows.routes.lightning_round_ending_three_way_tie."""
    response: TestResponse = client.get("/shows/lightning-round-ending-three-way-tie")
    assert response.status_code == 200
    assert b"Lightning Round Ending in a Three-Way Tie" in response.data
    assert b"Panelists" in response.data
    assert b"Final Score" in response.data


def test_lightning_round_starting_ending_three_way_tie(client: FlaskClient) -> None:
    """Testing shows.routes.lightning_round_starting_ending_three_way_tie."""
    response: TestResponse = client.get(
        "/shows/lightning-round-starting-ending-three-way-tie"
    )
    assert response.status_code == 200
    assert b"Lightning Round Starting and Ending in a Three-Way Tie" in response.data
    assert b"Panelists" in response.data
    assert b"Final Score" in response.data


def test_lightning_round_starting_three_way_tie(client: FlaskClient) -> None:
    """Testing shows.routes.lightning_round_starting_three_way_tie."""
    response: TestResponse = client.get("/shows/lightning-round-starting-three-way-tie")
    assert response.status_code == 200
    assert b"Lightning Round Starting in a Three-Way Tie" in response.data
    assert b"Panelists" in response.data
    assert b"Starting Score" in response.data


def test_lightning_round_starting_zero_points(client: FlaskClient) -> None:
    """Testing shows.routes.lightning_round_starting_zero_points."""
    response: TestResponse = client.get("/shows/lightning-round-starting-zero-points")
    assert response.status_code == 200
    assert b"Lightning Round Starting with Zero Points" in response.data
    assert b"Panelist" in response.data
    assert b"Rank" in response.data


def test_lightning_round_zero_correct(client: FlaskClient) -> None:
    """Testing shows.routes.lightning_round_zero_correct."""
    response: TestResponse = client.get("/shows/lightning-round-zero-correct")
    assert response.status_code == 200
    assert b"Lightning Round with Zero Correct Answers" in response.data
    assert b"Panelist" in response.data
    assert b"Rank" in response.data


def test_low_scoring_shows(client: FlaskClient) -> None:
    """Testing shows.routes.low_scoring_shows."""
    response: TestResponse = client.get("/shows/low-scoring-shows")
    assert response.status_code == 200
    assert b"Low Scoring Shows" in response.data
    assert b"Show Date" in response.data
    assert b"Panelists" in response.data


def testnot_my_job_guests_vs_bluff_the_listener_win_ratios(client: FlaskClient) -> None:
    """Testing shows.routes.not_my_job_vs_bluffs."""
    response: TestResponse = client.get(
        "/shows/not-my-job-guests-vs-bluff-the-listener-win-ratios"
    )
    assert response.status_code == 200
    assert b"Not My Job Guests" in response.data
    assert b"Bluff the Listener" in response.data
    assert b"Win %" in response.data


@pytest.mark.parametrize("sort", [None, "asc", "desc"])
def test_original_shows(client: FlaskClient, sort: str | None) -> None:
    """Testing shows.routes.original_shows."""
    response: TestResponse = client.get(
        "/shows/original-shows", query_string={"sort": sort}
    )
    assert response.status_code == 200
    assert b"Original Shows" in response.data
    assert b"Panelists" in response.data
    assert b"Guest" in response.data


def test_panel_gender_mix(client: FlaskClient) -> None:
    """Testing shows.routes.panel_gender_mix."""
    response: TestResponse = client.get("/shows/panel-gender-mix")
    assert response.status_code == 200
    assert b"Panel Gender Mix" in response.data
    assert b"3 W / 0 M" in response.data
    assert b"Total" in response.data


@pytest.mark.parametrize("sort", [None, "asc", "desc"])
def test_repeat_best_of_shows(client: FlaskClient, sort: str | None) -> None:
    """Testing shows.routes.repeat_best_of_shows."""
    response: TestResponse = client.get(
        "/shows/repeat-best-of-shows", query_string={"sort": sort}
    )
    assert response.status_code == 200
    assert b"Repeat Best Of Shows" in response.data
    assert b"Change sorting to" in response.data
    assert b"Guest" in response.data


@pytest.mark.parametrize("sort", [None, "asc", "desc"])
def test_repeat_shows(client: FlaskClient, sort: str | None) -> None:
    """Testing shows.routes.repeat_shows."""
    response: TestResponse = client.get(
        "/shows/repeat-shows", query_string={"sort": sort}
    )
    assert response.status_code == 200
    assert b"Repeat Shows" in response.data
    assert b"Change sorting to" in response.data
    assert b"Guest" in response.data


def test_search_shows_by_multiple_panelists(client: FlaskClient) -> None:
    """Testing shows.routes.search_shows_by_multiple_panelists (GET)."""
    response: TestResponse = client.get("/shows/search-shows-by-multiple-panelists")
    assert response.status_code == 200
    assert b"Search Shows by Multiple Panelists" in response.data
    assert b"Include Best Ofs" in response.data
    assert b"Panelist 1" in response.data
    assert b"Panelist 2" in response.data
    assert b"Panelist 3" in response.data


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
    assert b"Search Shows by Multiple Panelists" in response.data
    assert b"Include Best Ofs" in response.data
    assert b"Best Of" in response.data
    assert b"Repeat Of" in response.data
    assert b"Location" in response.data


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
    assert b"Search Shows by Multiple Panelists" in response.data
    assert b"Best Of" in response.data
    assert b"Repeat Of" in response.data
    assert b"Location" in response.data


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
    assert b"Search Shows by Multiple Panelists" in response.data
    assert b"Best Of" in response.data
    assert b"Repeat Of" in response.data
    assert b"Location" in response.data


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
    assert b"Search Shows by Multiple Panelists" in response.data
    assert b"Best Of" in response.data
    assert b"Repeat Of" in response.data
    assert b"Location" in response.data


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
    assert b"Search Shows by Multiple Panelists" in response.data
    assert b"Best Of" in response.data
    assert b"Repeat Of" in response.data
    assert b"Location" in response.data


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
    assert b"Search Shows by Multiple Panelists" in response.data
    assert b"Best Of" in response.data
    assert b"Repeat Of" in response.data
    assert b"Location" in response.data


def test_show_counts_by_year(client: FlaskClient) -> None:
    """Testing shows.routes.show_counts_by_year."""
    response: TestResponse = client.get("/shows/show-counts-by-year")
    assert response.status_code == 200
    assert b"Show Counts by Year" in response.data
    assert b"Best Of" in response.data
    assert b"Repeat Best Ofs" in response.data


def test_show_descriptions(client: FlaskClient) -> None:
    """Testing shows.routes.show_descriptions."""
    response: TestResponse = client.get("/shows/show-descriptions")
    assert response.status_code == 200
    assert b"Show Descriptions" in response.data
    assert b"Show Date" in response.data


def test_show_notes(client: FlaskClient) -> None:
    """Testing shows.routes.show_notes."""
    response: TestResponse = client.get("/shows/show-notes")
    assert response.status_code == 200
    assert b"Show Notes" in response.data
    assert b"Show Date" in response.data


def test_shows_with_guest_host(client: FlaskClient) -> None:
    """Testing shows.routes.shows_with_guest_host."""
    response: TestResponse = client.get("/shows/shows-with-guest-host")
    assert response.status_code == 200
    assert b"Shows with a Guest Host" in response.data
    assert b"Panelists" in response.data
    assert b"Guest(s)" in response.data


def test_shows_with_guest_host_scorekeeper(client: FlaskClient) -> None:
    """Testing shows.routes.shows_with_guest_host_scorekeeper."""
    response: TestResponse = client.get("/shows/shows-with-guest-host-scorekeeper")
    assert response.status_code == 200
    assert b"Shows with a Guest Host and a Guest Scorekeeper" in response.data
    assert b"Panelists" in response.data
    assert b"Guest(s)" in response.data


def test_shows_with_guest_scorekeeper(client: FlaskClient) -> None:
    """Testing shows.routes.shows_with_guest_scorekeeper."""
    response: TestResponse = client.get("/shows/shows-with-guest-scorekeeper")
    assert response.status_code == 200
    assert b"Shows with a Guest Scorekeeper" in response.data
    assert b"Panelists" in response.data
    assert b"Guest(s)" in response.data


def test_shows_with_perfect_panelist_scores(client: FlaskClient) -> None:
    """Testing shows.routes.shows_with_perfect_panelist_scores."""
    response: TestResponse = client.get("/shows/shows-with-perfect-panelist-scores")
    assert response.status_code == 200
    assert b"Shows with Perfect Panelist Scores"
    assert b"Show Date"
