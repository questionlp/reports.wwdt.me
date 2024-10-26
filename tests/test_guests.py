# Copyright (c) 2018-2024 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing Guests Module and Blueprint Views."""
from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_index(client: FlaskClient) -> None:
    """Testing guests.routes.index."""
    response: TestResponse = client.get("/guests/")
    assert response.status_code == 200
    assert b"Guests" in response.data
    assert b"Best Of Only Not My Job Guests" in response.data


def test_best_of_only(client: FlaskClient) -> None:
    """Testing guests.routes.best_of_only."""
    response: TestResponse = client.get("/guests/best-of-only")
    assert response.status_code == 200
    assert b"Best Of Only Not My Job Guests" in response.data
    assert b"Scoring Exception" in response.data


def test_most_appearances(client: FlaskClient) -> None:
    """Testing guests.routes.most_appearances."""
    response: TestResponse = client.get("/guests/most-appearances")
    assert response.status_code == 200
    assert b"Most Appearances" in response.data
    assert b"Regular" in response.data


def test_scoring_exceptions(client: FlaskClient) -> None:
    """Testing guests.routes.scoring_exceptions."""
    response: TestResponse = client.get("/guests/scoring-exceptions")
    assert response.status_code == 200
    assert b"Not My Job Scoring Exceptions" in response.data
    assert b"Show Notes" in response.data


def test_three_pointers(client: FlaskClient) -> None:
    """Testing guests.routes.three_pointers."""
    response: TestResponse = client.get("/guests/three-pointers")
    assert response.status_code == 200
    assert b"Not My Job Three Pointers" in response.data
    assert b"Scoring Exception" in response.data
