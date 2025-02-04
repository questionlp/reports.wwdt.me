# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing Hosts Module and Blueprint Views."""

from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_index(client: FlaskClient) -> None:
    """Testing hosts.routes.index."""
    response: TestResponse = client.get("/hosts/")
    assert response.status_code == 200
    assert b"Hosts" in response.data
    assert b"Appearance Summary" in response.data


def test_appearance_summary(client: FlaskClient) -> None:
    """Testing hosts.routes.appearance_summary."""
    response: TestResponse = client.get("/hosts/appearance-summary")
    assert response.status_code == 200
    assert b"Appearance Summary" in response.data
    assert b"Regular Shows" in response.data
    assert b"All Shows" in response.data
