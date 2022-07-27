# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""Testing Main Redirects Module and Blueprint Views"""
import pytest


def test_favicon(client):
    """Testing main_redirects.favicon"""
    response = client.get("/favicon.ico")
    assert response.status_code == 301
    assert response.location
