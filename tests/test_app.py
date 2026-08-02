import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    original = copy.deepcopy(app_module.activities)
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original))
    yield
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original))


@pytest.fixture
def client():
    return TestClient(app_module.app)


def test_unregister_participant_from_activity(client):
    signup_response = client.post(
        "/activities/Chess Club/signup?email=student@example.com"
    )
    assert signup_response.status_code == 200

    remove_response = client.delete(
        "/activities/Chess Club/signup?email=student@example.com"
    )

    assert remove_response.status_code == 200
    assert "student@example.com" not in app_module.activities["Chess Club"]["participants"]
