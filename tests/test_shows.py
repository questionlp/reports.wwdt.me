# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""Testing Shows Module and Blueprint Views"""
import pytest


def test_index(client):
    """Testing shows.index"""
    response = client.get("/shows")
    assert response.status_code == 200
    assert b"Shows Reports" in response.data
    assert b"All Shows" in response.data
    assert b"Original Shows" in response.data
