# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing Locations Redirects Module and Blueprint Views."""

from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_index(client: FlaskClient) -> None:
    """Testing locations.redirects.index."""
    response: TestResponse = client.get("/location")
    assert response.status_code == 301
    assert response.location

    response: TestResponse = client.get("/locations")
    assert response.status_code == 301
    assert response.location


def test_average_scores(client: FlaskClient) -> None:
    """Testing locations.redirects.average_scores_by_location."""
    response: TestResponse = client.get("/location/average_scores")
    assert response.status_code == 301
    assert response.location

    response: TestResponse = client.get("/locations/average-scores")
    assert response.status_code == 301
    assert response.location
