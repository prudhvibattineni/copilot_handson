from fastapi.testclient import TestClient
import pytest

from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Ensure at least one known activity exists
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = "test_user@example.com"

    # ensure not already in participants
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # signup
    signup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_resp.status_code == 200
    assert email in activities[activity]["participants"]

    # duplicate signup should fail
    dup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert dup_resp.status_code == 400

    # unregister
    del_resp = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert del_resp.status_code == 200
    assert email not in activities[activity]["participants"]


def test_unregister_nonexistent():
    activity = "Chess Club"
    email = "not_in_list@example.com"

    # make sure it's not there
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    resp = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert resp.status_code == 404


def test_signup_activity_not_found():
    resp = client.post("/activities/Nonexistent%20Activity/signup?email=a@b.com")
    assert resp.status_code == 404


def test_unregister_activity_not_found():
    resp = client.delete("/activities/Nonexistent%20Activity/unregister?email=a@b.com")
    assert resp.status_code == 404
