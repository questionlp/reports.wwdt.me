# -*- coding: utf-8 -*-
# vim: set noai syntax=python ts=4 sw=4:
#
# Copyright (c) 2018-2023 Linh Pham
# reports.wwdt.me is released under the terms of the Apache License 2.0
"""pytest conftest.py File"""
from flask import Flask
import pytest

from app import create_app


@pytest.fixture
def client():
    app: Flask = create_app()
    with app.test_client() as client:
        yield client
