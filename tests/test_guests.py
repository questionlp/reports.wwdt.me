# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""Testing Guests Module and Blueprint Views"""
import pytest


def test_index(client):
    """Testing guests.index"""
    response = client.get("/guests")
    assert response.status_code == 200
    assert b"Guests Reports" in response.data
    assert b"Best Of Only Not My Job Guests" in response.data


def test_best_of_only(client):
    """Testing guests.best_of_only"""
    response = client.get("/guests/best-of-only")
    assert response.status_code == 200
    assert b"Best Of Only Not My Job Guests" in response.data
    assert b"Scoring Exception" in response.data


def test_most_appearances(client):
    """Testing guests.most_appearances"""
    response = client.get("/guests/most-appearances")
    assert response.status_code == 200
    assert b"Most Appearances" in response.data
    assert b"Regular" in response.data


def test_scoring_exceptions(client):
    """Testing guests.scoring_exceptions"""
    response = client.get("/guests/scoring-exceptions")
    assert response.status_code == 200
    assert b"Not My Job Scoring Exceptions" in response.data
    assert b"Show Notes" in response.data


def test_three_pointers(client):
    """Testing guests.three_pointers"""
    response = client.get("/guests/three-pointers")
    assert response.status_code == 200
    assert b"Not My Job Three Pointers" in response.data
    assert b"Scoring Exception" in response.data
