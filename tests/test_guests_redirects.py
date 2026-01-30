# Copyright (c) 2018-2026 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing Guests Redirects Module and Blueprint Views."""

from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_index(client: FlaskClient) -> None:
    """Testing guests.redirects.index."""
    response: TestResponse = client.get("/guest")
    assert response.status_code == 301
    assert response.location

    response: TestResponse = client.get("/guests")
    assert response.status_code == 301
    assert response.location


def test_best_of_only(client: FlaskClient) -> None:
    """Testing guests.redirects.best_of_only_not_my_job_guests."""
    response: TestResponse = client.get("/guest/best_of_only")
    assert response.status_code == 301
    assert response.location

    response: TestResponse = client.get("/guests/best-of-only")
    assert response.status_code == 301
    assert response.location


def test_most_appearances(client: FlaskClient) -> None:
    """Testing guests.redirects.most_appearances."""
    response: TestResponse = client.get("/guest/most_appearances")
    assert response.status_code == 301
    assert response.location


def test_scoring_exceptions(client: FlaskClient) -> None:
    """Testing guests.redirects.not_my_job_scoring_exceptions."""
    response: TestResponse = client.get("/guest/scoring_exceptions")
    assert response.status_code == 301
    assert response.location

    response: TestResponse = client.get("/guests/scoring-exceptions")
    assert response.status_code == 301
    assert response.location


def test_three_pointers(client: FlaskClient) -> None:
    """Testing guests.redirects.not_my_job_three_pointers."""
    response: TestResponse = client.get("/guest/three_pointers")
    assert response.status_code == 301
    assert response.location

    response: TestResponse = client.get("/guests/three-pointers")
    assert response.status_code == 301
    assert response.location
