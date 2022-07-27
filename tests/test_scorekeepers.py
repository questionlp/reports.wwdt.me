# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""Testing Scorekeepers Module and Blueprint Views"""
import pytest


def test_index(client):
    """Testing scorekeepers.index"""
    response = client.get("/scorekeepers")
    assert response.status_code == 200
    assert b"Scorekeepers Reports" in response.data
    assert b"Appearance Summary" in response.data
