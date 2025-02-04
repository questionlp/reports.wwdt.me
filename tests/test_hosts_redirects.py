# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing Hosts Redirects Module and Blueprint Views."""

from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_index(client: FlaskClient) -> None:
    """Testing hosts.redirects.index."""
    response: TestResponse = client.get("/host")
    assert response.status_code == 301
    assert response.location

    response: TestResponse = client.get("/hosts")
    assert response.status_code == 301
    assert response.location


def test_appearance_summary(client: FlaskClient) -> None:
    """Testing hosts.redirects.index."""
    response: TestResponse = client.get("/host/appearance_summary")
    assert response.status_code == 301
    assert response.location
