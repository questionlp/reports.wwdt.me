# Copyright (c) 2018-2025 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing Main Redirects Module and Blueprint Views."""
from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_favicon(client: FlaskClient) -> None:
    """Testing main.redirects.favicon."""
    response: TestResponse = client.get("/favicon.ico")
    assert response.status_code == 301
    assert response.location
