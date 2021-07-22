#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

import main


@pytest.fixture()
def client():
    main.app.testing = True
    client = main.app.test_client()
    return client


def test_index(client):
    r = client.get('/')
    assert r.status_code == 200
    assert 'Website of' in r.data.decode('utf-8')


def test_bio(client):
    r = client.get('/bio')
    assert r.status_code == 200
    assert 'Biography of' in r.data.decode('utf-8')
    assert 'Work Experience' in r.data.decode('utf-8')


def test_bio_ja(client):
    r = client.get('/bio.ja')
    assert r.status_code == 200
    assert 'Biography of' in r.data.decode('utf-8')
    assert '所属・経歴' in r.data.decode('utf-8')


def test_cv(client):
    r = client.get('/cv')
    assert r.status_code == 302


def test_cv_ja(client):
    r = client.get('/cv.ja')
    assert r.status_code == 302
