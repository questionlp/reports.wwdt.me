# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""Testing Hosts Module and Blueprint Views"""
import pytest


def test_index(client):
    """Testing hosts.index"""
    response = client.get("/hosts")
    assert response.status_code == 200
    assert b"Hosts Reports" in response.data
    assert b"Appearance Summary" in response.data


def test_appearance_summary(client):
    """Testing hosts.appearance_summary"""
    response = client.get("/hosts/appearance-summary")
    assert response.status_code == 200
    assert b"Appearance Summary" in response.data
    assert b"Regular Shows" in response.data
    assert b"All Shows" in response.data
