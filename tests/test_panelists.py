# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""Testing Panelists Module and Blueprint Views"""
import pytest


def test_index(client):
    """Testing panelists.index"""
    response = client.get("/panelists")
    assert response.status_code == 200
    assert b"Panelists Reports" in response.data
    assert b"Aggregate Scores" in response.data


def test_aggregate_scores(client):
    """Testing panelists.aggregate_scores"""
    response = client.get("/panelists/aggregate-scores")
    assert response.status_code == 200
    assert b"Aggregate Score Statistics" in response.data
    assert b"Aggregate Score Spread" in response.data


def test_appearances_by_year(client):
    """Testing panelists.appearances_by_year"""
    response = client.get("/panelists/appearances-by-year")
    assert response.status_code == 200
    assert b"Appearances by Year" in response.data
    assert b"Total" in response.data


def test_bluff_stats(client):
    """Testing panelists.bluff_stats"""
    response = client.get("/panelists/bluff-stats")
    assert response.status_code == 200
    assert b"Bluff the Listener Stats" in response.data
    assert b"Unique Best Of" in response.data


def test_debut_by_year(client):
    """Testing panelists.debut_by_year"""
    response = client.get("/panelists/debut-by-year")
    assert response.status_code == 200
    assert b"Debut by Year" in response.data
    assert b"# of Regular Appearances" in response.data


def test_first_most_recent_appearances(client):
    """Testing panelists.first_most_recent_appearances"""
    response = client.get("/panelists/first-most-recent-appearances")
    assert response.status_code == 200
    assert b"First and Most Recent Appearances" in response.data
    assert b"Regular Shows" in response.data
    assert b"All Shows" in response.data


def test_gender_stats(client):
    """Testing panelists.gender_stats"""
    response = client.get("/panelists/gender-stats")
    assert response.status_code == 200
    assert b"Statistics by Gender" in response.data
    assert b"Std Dev" in response.data


def test_losing_streaks(client):
    """Testing panelists.losing_streaks"""
    response = client.get("/panelists/losing-streaks")
    assert response.status_code == 200
    assert b"Losing Streaks" in response.data
    assert b"All Losses" in response.data
    assert b"Third Place Losses" in response.data


def test_panelist_pvp_get(client):
    """Testing panelists."""
    response = client.get("/panelists/panelist-pvp")
    assert response.status_code == 200
    assert b"Panelist vs Panelist" in response.data
    assert b"Please chose a panelist" in response.data


@pytest.mark.parametrize("panelist_slug", ["faith-salie"])
def test_panelist_pvp_post(client, panelist_slug: str):
    """Testing panelists."""
    response = client.post("/panelists/panelist-pvp", data={"panelist": panelist_slug})
    assert response.status_code == 200
    assert b"Panelist vs Panelist" in response.data
    assert panelist_slug.encode("utf-8") in response.data
    assert b"Ranked vs" in response.data


def test_panelist_pvp_all(client):
    """Testing panelists.panelist_pvp_all"""
    response = client.get("/panelists/panelist-pvp/all")
    assert response.status_code == 200
    assert b"Panelist vs Panelist: All" in response.data
    assert b"Ranked vs" in response.data
    assert b"Total" in response.data


def test_panelist_pvp_scoring_get(client):
    """Testing panelists.panelist_pvp_scoring"""
    response = client.get("/panelists/panelist-vs-panelist-scoring")
    assert response.status_code == 200
    assert b"Panelist vs Panelist Scoring" in response.data
    assert b"Please chose a panelist" in response.data


@pytest.mark.parametrize("panelist_1, panelist_2", [("adam-felber", "faith-salie")])
def test_panelist_pvp_scoring_post(client, panelist_1: str, panelist_2: str):
    """Testing panelists.panelist_pvp_scoring"""
    response = client.post(
        "/panelists/panelist-vs-panelist-scoring",
        data={
            "panelist_1": panelist_1,
            "panelist_2": panelist_2,
        },
    )
    assert response.status_code == 200
    assert b"Panelist vs Panelist Scoring" in response.data
    assert panelist_1.encode("utf-8") in response.data
    assert panelist_2.encode("utf-8") in response.data
    assert b"Score" in response.data
    assert b"Rank" in response.data


def test_rankings_summary(client):
    """Testing panelists.rankings_summary"""
    response = client.get("/panelists/rankings-summary")
    assert response.status_code == 200
    assert b"Rankings Summary" in response.data
    assert b"First" in response.data
    assert b"Second" in response.data


def test_single_appearance(client):
    """Testing panelists.single_appearance"""
    response = client.get("/panelists/single-appearance")
    assert response.status_code == 200
    assert b"Single Appearance" in response.data
    assert b"Show Date" in response.data


def test_stats_summary(client):
    """Testing panelists.stats_summary"""
    response = client.get("/panelists/stats-summary")
    assert response.status_code == 200
    assert b"Statistics Summary" in response.data
    assert b"Std Dev" in response.data


def test_win_streaks(client):
    """Testing panelists.win_streaks"""
    response = client.get("/panelists/win-streaks")
    assert response.status_code == 200
    assert b"Win Streaks" in response.data
    assert b"Outright Wins" in response.data
    assert b"Wins with Draws" in response.data
