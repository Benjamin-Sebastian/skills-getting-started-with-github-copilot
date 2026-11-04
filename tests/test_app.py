from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


def test_get_activities_returns_activity_data():
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert expected_activity in response.json()
    assert "participants" in response.json()[expected_activity]


def test_signup_adds_participant_to_activity():
    # Arrange
    activities["Chess Club"]["participants"] = [
        "michael@mergington.edu",
    ]
    new_email = "student@mergington.edu"

    # Act
    response = client.post(
        "/activities/Chess Club/signup?email=student@mergington.edu"
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {new_email} for Chess Club"
    }
    assert new_email in activities["Chess Club"]["participants"]


def test_duplicate_signup_returns_400():
    # Arrange
    activities["Chess Club"]["participants"] = [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]

    # Act
    response = client.post(
        "/activities/Chess Club/signup?email=daniel@mergington.edu"
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_removes_email_from_activity():
    # Arrange
    activities["Chess Club"]["participants"] = [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]

    # Act
    response = client.delete(
        "/activities/Chess Club/unregister?email=daniel@mergington.edu"
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": "Removed daniel@mergington.edu from Chess Club"
    }
    assert "daniel@mergington.edu" not in activities["Chess Club"]["participants"]
