# Copyright (c) 2018-2026 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0
#
# vim: set noai syntax=python ts=4 sw=4:
"""Testing Errors Module and Blueprint Views."""

from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_not_found(client: FlaskClient) -> None:
    """Testing errors.not_found."""
    response: TestResponse = client.get("/bad-url")
    assert response.status_code == 404
