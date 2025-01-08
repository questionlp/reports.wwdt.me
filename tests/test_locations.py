# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing Locations Module and Blueprint Views."""
from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_index(client: FlaskClient) -> None:
    """Testing locations.routes.index."""
    response: TestResponse = client.get("/locations/")
    assert response.status_code == 200
    assert b"Locations" in response.data
    assert b"Average Scores by Location" in response.data


def test_average_scores_by_location(client: FlaskClient) -> None:
    """Testing locations.routes.average_scores_by_location."""
    response: TestResponse = client.get("/locations/average-scores-by-location")
    assert response.status_code == 200
    assert b"Average Scores by Location" in response.data
    assert b"Venue" in response.data
    assert b"Average Total" in response.data
