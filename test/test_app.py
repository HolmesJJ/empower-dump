import pytest
import requests
import unittest

CONFIG = {
    "HOST": "127.0.0.1",
    "PORT": 5000,
}

API = {
    "REFRESH": "http://" + CONFIG["HOST"] + ":" + str(CONFIG["PORT"]) + "/api/refresh",
    "LOGIN": "http://" + CONFIG["HOST"] + ":" + str(CONFIG["PORT"]) + "/api/login",
    "SUMMARY": "http://" + CONFIG["HOST"] + ":" + str(CONFIG["PORT"]) + "/api/summary",
    "RANK": "http://" + CONFIG["HOST"] + ":" + str(CONFIG["PORT"]) + "/api/rank"
}

TOKEN = {
    "ACCESS": "",
    "REFRESH": ""
}


def login():
    res = requests.post(API["LOGIN"], json={
        "username": "max",
        "password": "max"
    })
    data = res.json()
    TOKEN["ACCESS"] = data["token"]["access"]
    TOKEN["REFRESH"] = data["token"]["refresh"]


@pytest.fixture(scope="class")
def test_refresh_token_success():
    login()
    res = requests.post(API["REFRESH"], headers={
        "Authorization": "Bearer " + TOKEN["REFRESH"]
    }, json={})
    assert res.status_code == 200
    assert res.json()["code"] == 1
    assert res.json()["token"]["access"] != TOKEN["ACCESS"]


def test_login_success():
    res = requests.post(API["LOGIN"], json={
        "username": "max",
        "password": "max"
    })
    assert res.status_code == 200
    assert res.json()["code"] == 1


def test_login_missing_parameters():
    res = requests.post(API["LOGIN"], json={})
    assert res.status_code == 200
    assert res.json()["code"] == 0
    assert res.json()["message"] == "Missing parameters"


def test_login_failure():
    res = requests.post(API["LOGIN"], json={
        "username": "max",
        "password": "max1"
    })
    assert res.status_code == 200
    assert res.json()["code"] == 0


def test_summary_success():
    login()
    res = requests.post(API["SUMMARY"], headers={
        "Authorization": "Bearer " + TOKEN["ACCESS"]
    }, json={
        "id": "6099121fe5318c9103f1689f",
        "date": "2021-04-21"
    })
    assert res.status_code == 200
    assert res.json()["code"] == 1


def test_summary_missing_parameters():
    login()
    res = requests.post(API["SUMMARY"], headers={
        "Authorization": "Bearer " + TOKEN["ACCESS"]
    }, json={})
    assert res.status_code == 200
    assert res.json()["code"] == 0
    assert res.json()["message"] == "Missing parameters"


def test_summary_invalid_date():
    login()
    res = requests.post(API["SUMMARY"], headers={
        "Authorization": "Bearer " + TOKEN["ACCESS"]
    }, json={
        "id": "6099121fe5318c9103f1689f",
        "date": "2021-04-31"
    })
    assert res.status_code == 200
    assert res.json()["code"] == 0
    assert res.json()["message"] == "Error date format"


def test_summary_unauthorized():
    res = requests.post(API["SUMMARY"], json={})
    assert res.status_code == 401
    assert res.json()["code"] == 0
    assert res.json()["message"] == "Please login"


def test_summary_invalid_token():
    res = requests.post(API["SUMMARY"], headers={
        "Authorization": "Bearer " + TOKEN["REFRESH"]
    }, json={})
    assert res.status_code == 401
    assert res.json()["code"] == 0
    assert res.json()["message"] == "Token is invalid"


def test_rank_success():
    login()
    res = requests.get(API["RANK"], headers={
        "Authorization": "Bearer " + TOKEN["ACCESS"]
    })
    assert res.status_code == 200
    assert res.json()["message"] == "success"
    assert res.json()["data"] == [
        'phangjiekie', 'epg002', 'etp014', 'etp022', 'jimmya', 'epg005', 'etp001', 'epg010', 'etp013', 'etp002',
        'epg011', 'etp018', 'etp021', 'etp009', 'etp008', 'epg006', 'etp007', 'epg009', 'etp010ah', 'epg001',
        'epg019', 'epg015', 'etp011', 'ebd003', 'etp016', 'etp026', 'epg022', 'etp024', 'epg003', 'epg012',
        'ebd006', 'max', 'etp025', 'epg023', 'etp003', 'epg021', 'epg007', 'ebd009', 'epg004', 'etp034',
        'epg016', 'ebd010', 'epg017', 'etp019', 'etp033', 'etp030', 'etp015', 'epg018', 'etp032', 'ebd001',
        'epg024', 'epg013', 'etp027', 'epg025', 'epg008', 'ebd007', 'etp017', 'etp006', 'ebd008', 'etp012',
        'epg029', 'ebd004', 'epg014', 'ebd013', 'etp031', 'ebd012', 'epg020', 'etp020', 'ebd014', 'etp028',
        'epg027', 'epg026', 'etp023', 'epg028', 'etp029', 'abc', 'ebd011', 'ebd002', 'etp004']


def test_rank_unauthorized():
    res = requests.get(API["RANK"], json={})
    assert res.status_code == 401
    assert res.json()["code"] == 0
    assert res.json()["message"] == "Please login"


def test_rank_invalid_token():
    res = requests.get(API["RANK"], headers={
        "Authorization": "Bearer " + TOKEN["REFRESH"]
    }, json={})
    assert res.status_code == 401
    assert res.json()["code"] == 0
    assert res.json()["message"] == "Token is invalid"


if __name__ == "__main__":
    unittest.main()
