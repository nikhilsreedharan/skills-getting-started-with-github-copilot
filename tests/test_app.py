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
    # Arrange
    activity_name = "Chess Club"
    email = "student@example.com"

    # Act
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    remove_response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert signup_response.status_code == 200
    assert remove_response.status_code == 200
    assert email not in app_module.activities[activity_name]["participants"]
