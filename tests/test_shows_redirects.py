# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2022 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""Testing Shows Redirects Module and Blueprint Views"""
from flask.testing import FlaskClient
from werkzeug.test import TestResponse


def test_index(client: FlaskClient) -> None:
    """Testing shows.redirects.index"""
    response: TestResponse = client.get("/show")
    assert response.status_code == 301
    assert response.location

    response: TestResponse = client.get("/shows")
    assert response.status_code == 301
    assert response.location


def test_all_shows(client: FlaskClient) -> None:
    """Testing shows.redirects.all_shows"""
    response: TestResponse = client.get("/show/all_shows")
    assert response.status_code == 301
    assert response.location


def test_all_shows_asc(client: FlaskClient) -> None:
    """Testing shows.redirects.all_shows_asc"""
    response: TestResponse = client.get("/show/all_shows/asc")
    assert response.status_code == 301
    assert response.location

    response: TestResponse = client.get("/shows/all-shows/asc")
    assert response.status_code == 301
    assert response.location


def test_all_shows_desc(client: FlaskClient) -> None:
    """Testing shows.redirects.all_shows_desc"""
    response: TestResponse = client.get("/show/all_shows/desc")
    assert response.status_code == 301
    assert response.location

    response: TestResponse = client.get("/shows/all-shows/desc")
    assert response.status_code == 301
    assert response.location


def test_all_women_panel(client: FlaskClient) -> None:
    """Testing shows.redirects.all_women_panel"""
    response: TestResponse = client.get("/show/all_women_panel")
    assert response.status_code == 301
    assert response.location


def test_guest_host(client: FlaskClient) -> None:
    """Testing shows.redirects.guest_host"""
    response: TestResponse = client.get("/show/guest_host")
    assert response.status_code == 301
    assert response.location

    response: TestResponse = client.get("/show/guest_hosts")
    assert response.status_code == 301
    assert response.location

    response: TestResponse = client.get("/shows/guest-hosts")
    assert response.status_code == 301
    assert response.location


def test_guest_scorekeeper(client: FlaskClient) -> None:
    """Testing shows.redirects.guest_scorekeeper"""
    response: TestResponse = client.get("/show/guest_scorekeeper")
    assert response.status_code == 301
    assert response.location

    response: TestResponse = client.get("/show/guest_scorekeepers")
    assert response.status_code == 301
    assert response.location

    response: TestResponse = client.get("/shows/guest-scorekeepers")
    assert response.status_code == 301
    assert response.location


def test_high_scoring(client: FlaskClient) -> None:
    """Testing shows.redirects.high_scoring"""
    response: TestResponse = client.get("/show/high_scoring")
    assert response.status_code == 301
    assert response.location


def test_highest_score_equal_sum_other_scores(client: FlaskClient) -> None:
    """Testing shows.redirects.highest_score_equal_sum_other_scores"""
    response: TestResponse = client.get("/show/high_score_equal_sum_other_scores")
    assert response.status_code == 301
    assert response.location


def test_lightning_round_end_three_way_tie(client: FlaskClient) -> None:
    """Testing shows.redirects.lightning_round_end_three_way_tie"""
    response: TestResponse = client.get("/show/lightning_round_end_three_way_tie")
    assert response.status_code == 301
    assert response.location


def test_lightning_round_start_end_three_way_tie(client: FlaskClient) -> None:
    """Testing shows.redirects.lightning_round_start_end_three_way_tie"""
    response: TestResponse = client.get("/show/lightning_round_start_end_three_way_tie")
    assert response.status_code == 301
    assert response.location


def test_lightning_round_start_zero_points(client: FlaskClient) -> None:
    """Testing shows.redirects.lightning_round_start_zero_points"""
    response: TestResponse = client.get("/show/lighting_round_start_zero")
    assert response.status_code == 301
    assert response.location


def test_lightning_round_zero_correct(client: FlaskClient) -> None:
    """Testing shows.redirects.lightning_round_zero_correct"""
    response: TestResponse = client.get("/show/lightning_round_zero_correct")
    assert response.status_code == 301
    assert response.location


def test_low_scoring(client: FlaskClient) -> None:
    """Testing shows.redirects.low_scoring"""
    response: TestResponse = client.get("/show/low_scoring")
    assert response.status_code == 301
    assert response.location


def test_original_shows(client: FlaskClient) -> None:
    """Testing shows.redirects.original_shows"""
    response: TestResponse = client.get("/show/original_shows")
    assert response.status_code == 301
    assert response.location


def test_original_shows_asc(client: FlaskClient) -> None:
    """Testing shows.redirects.original_shows_asc"""
    response: TestResponse = client.get("/show/original_shows/asc")
    assert response.status_code == 301
    assert response.location

    response: TestResponse = client.get("/shows/original-shows/asc")
    assert response.status_code == 301
    assert response.location


def test_original_shows_desc(client: FlaskClient) -> None:
    """Testing shows.redirects.original_shows_desc"""
    response: TestResponse = client.get("/show/original_shows/desc")
    assert response.status_code == 301
    assert response.location

    response: TestResponse = client.get("/shows/original-shows/desc")
    assert response.status_code == 301
    assert response.location


def test_panel_gender_mix(client: FlaskClient) -> None:
    """Testing shows.redirects.panel_gender_mix"""
    response: TestResponse = client.get("/show/panel_gender_mix")
    assert response.status_code == 301
    assert response.location


def test_search_multiple_panelists(client: FlaskClient) -> None:
    """Testing shows.redirects.search_multiple_panelists"""
    response: TestResponse = client.get("/show/search_multiple_panelists")
    assert response.status_code == 301
    assert response.location


def test_search_multiple_panelists_post(client: FlaskClient) -> None:
    """Testing shows.redirects.search_multiple_panelists (POST)"""
    response: TestResponse = client.post(
        "/show/search_multiple_panelists",
        data={
            "panelist_1": "",
            "panelist_2": "",
            "panelist_3": "",
        },
    )
    assert response.status_code == 301
    assert response.location


def test_counts_by_year(client: FlaskClient) -> None:
    """Testing shows.redirects.counts_by_year"""
    response: TestResponse = client.get("/show/counts_by_year")
    assert response.status_code == 301
    assert response.location

    response: TestResponse = client.get("/show/show_counts_by_year")
    assert response.status_code == 301
    assert response.location

    response: TestResponse = client.get("/shows/counts_by_year")
    assert response.status_code == 301
    assert response.location

    response: TestResponse = client.get("/shows/show_counts_by_year")
    assert response.status_code == 301
    assert response.location

    response: TestResponse = client.get("/shows/show-counts-by-year")
    assert response.status_code == 301
    assert response.location
