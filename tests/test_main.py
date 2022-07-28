# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""Testing Main Routes Module and Blueprint Views"""
from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_index(client: FlaskClient) -> None:
    """Testing main.index"""
    response: TestResponse = client.get("/")
    assert response.status_code == 200
    assert b"Wait Wait... Don't Tell Me! Reports" in response.data
    assert b"Available Report Categories" in response.data


def test_robots_txt(client: FlaskClient) -> None:
    """Testing main.robots_txt"""
    response: TestResponse = client.get("/robots.txt")
    assert response.status_code == 200
    assert b"Sitemap:" in response.data