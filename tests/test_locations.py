# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing Locations Module and Blueprint Views."""

import pytest
from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_index(client: FlaskClient) -> None:
    """Testing locations.routes.index."""
    response: TestResponse = client.get("/locations/")
    assert response.status_code == 200
    assert b"Locations" in response.data
    assert b"Average Scores by Location" in response.data


def test_home_vs_away(client: FlaskClient) -> None:
    """Testing locations.routes.home_vs_away."""
    response: TestResponse = client.get("/locations/home-vs-away")
    assert response.status_code == 200
    assert b"Home vs Away" in response.data
    assert b"Year" in response.data
    assert b"Home" in response.data
    assert b"Away" in response.data


def test_average_scores_by_location(client: FlaskClient) -> None:
    """Testing locations.routes.average_scores_by_location."""
    response: TestResponse = client.get("/locations/average-scores-by-location")
    assert response.status_code == 200
    assert b"Average Scores by Location" in response.data
    assert b"Venue" in response.data
    assert b"Average Total" in response.data


def test_recordings_by_year(client: FlaskClient) -> None:
    """Testing locations.routes.recordings_by_year."""
    response: TestResponse = client.get("/locations/recordings-by-year")
    assert response.status_code == 200
    assert b"Recordings by Year" in response.data
    assert b"Select a Location" in response.data


@pytest.mark.parametrize(
    "location_slug",
    [
        "studebaker-theater-chicago-il",
        "arlene-schnitzer-concert-hall-portland-or",
    ],
)
def test_recordings_by_year_post(client: FlaskClient, location_slug: str) -> None:
    """Testing locations.routes.recordings_by_year (POST)."""
    response: TestResponse = client.post(
        "/locations/recordings-by-year", data={"location": location_slug}
    )
    assert response.status_code == 200
    assert b"Recordings by Year" in response.data
    assert location_slug.encode("utf-8") in response.data
    assert b"Repeat Of" in response.data


def test_recording_counts_by_location(client: FlaskClient) -> None:
    """Testing locations.routes.recording_counts_by_location."""
    response: TestResponse = client.get("/locations/recording-counts-by-location")
    assert response.status_code == 200
    assert b"Recording Counts by Location" in response.data
    assert b"Venue" in response.data
    assert b"Regular Shows" in response.data


def test_recording_counts_by_state(client: FlaskClient) -> None:
    """Testing locations.routes.recording_counts_by_state."""
    response: TestResponse = client.get("/locations/recording-counts-by-state")
    assert response.status_code == 200
    assert b"Recording Counts by State" in response.data
    assert b"State" in response.data
    assert b"Regular Shows" in response.data


def test_recording_counts_by_year(client: FlaskClient) -> None:
    """Testing locations.routes.recording_counts_by_year."""
    response: TestResponse = client.get("/locations/recording-counts-by-year")
    assert response.status_code == 200
    assert b"Recording Counts by Year" in response.data
    assert b"Venue" in response.data
    assert b"Regular Shows" in response.data
