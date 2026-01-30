# Copyright (c) 2018-2026 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing Guests Module and Blueprint Views."""

import pytest
from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_index(client: FlaskClient) -> None:
    """Testing guests.routes.index."""
    response: TestResponse = client.get("/guests/")
    assert response.status_code == 200
    assert b"Guests" in response.data
    assert b"Best Of Only Not My Job Guests" in response.data


def test_appearances_by_year(client: FlaskClient) -> None:
    """Testing guests.routes.appearances_by_year."""
    response: TestResponse = client.get("/guests/appearances-by-year")
    assert response.status_code == 200
    assert b"Appearances by Year" in response.data
    assert b"Select a Year" in response.data


@pytest.mark.parametrize("year", [1998, 2018])
def test_appearances_by_year_post(client: FlaskClient, year: int) -> None:
    """Testing guests.routes.appearances_by_year (POST)."""
    response: TestResponse = client.post(
        "/guests/appearances-by-year",
        data={"year": year},
    )
    assert response.status_code == 200
    assert b"Appearances by Year" in response.data
    assert b"Select a Year" in response.data
    assert b"Show Date" in response.data
    assert b"Scoring Exception" in response.data


def test_best_of_only_not_my_job_guests(client: FlaskClient) -> None:
    """Testing guests.routes.best_of_only_not_my_job_guests."""
    response: TestResponse = client.get("/guests/best-of-only-not-my-job-guests")
    assert response.status_code == 200
    assert b"Best Of Only Not My Job Guests" in response.data
    assert b"Scoring Exception" in response.data


def test_most_appearances(client: FlaskClient) -> None:
    """Testing guests.routes.most_appearances."""
    response: TestResponse = client.get("/guests/most-appearances")
    assert response.status_code == 200
    assert b"Most Appearances" in response.data
    assert b"Regular" in response.data


def test_not_my_job_guests_missing_scores(client: FlaskClient) -> None:
    """Testing guests.routes.not_my_job_missing_scores."""
    response: TestResponse = client.get("/guests/not-my-job-guests-missing-scores")
    assert response.status_code == 200
    assert b"Not My Job Guests with Missing Scores" in response.data


def test_not_my_job_scoring_exceptions(client: FlaskClient) -> None:
    """Testing guests.routes.not_my_job_scoring_exceptions."""
    response: TestResponse = client.get("/guests/not-my-job-scoring-exceptions")
    assert response.status_code == 200
    assert b"Not My Job Scoring Exceptions" in response.data
    assert b"Show Notes" in response.data


def test_not_my_job_three_pointers(client: FlaskClient) -> None:
    """Testing guests.routes.not_my_job_three_pointers."""
    response: TestResponse = client.get("/guests/not-my-job-three-pointers")
    assert response.status_code == 200
    assert b"Not My Job Three Pointers" in response.data
    assert b"Scoring Exception" in response.data


def test_wins_by_year(client: FlaskClient) -> None:
    """Testing guests.routes.wins_by_year."""
    response: TestResponse = client.get("/guests/wins-by-year")
    assert response.status_code == 200
    assert b"Wins by Year" in response.data
    assert b"Select a Year" in response.data


@pytest.mark.parametrize("year", [1998, 2018])
def test_wins_by_year_post(client: FlaskClient, year: int) -> None:
    """Testing guests.routes.wins_by_year (POST)."""
    response: TestResponse = client.post(
        "/guests/wins-by-year",
        data={"year": year},
    )
    assert response.status_code == 200
    assert b"Wins by Year" in response.data
    assert b"Select a Year" in response.data
    assert b"Show Date" in response.data
    assert b"Scoring Exception" in response.data
