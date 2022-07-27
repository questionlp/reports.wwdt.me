# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""Testing Locations Module and Blueprint Views"""
import pytest


def test_index(client):
    """Testing locations.index"""
    response = client.get("/locations")
    assert response.status_code == 200
    assert b"Locations Reports" in response.data
    assert b"Average Score by Location" in response.data


def test_average_scores(client):
    """Testing locations.average_scores"""
    response = client.get("/locations/average-scores")
    assert response.status_code == 200
    assert b"Average Score by Location" in response.data
    assert b"Venue" in response.data
    assert b"Average Total" in response.data
