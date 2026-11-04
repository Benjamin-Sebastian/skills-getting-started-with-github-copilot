from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activities["Chess Club"]["participants"] = [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]

    response = client.delete(
        "/activities/Chess Club/unregister?email=daniel@mergington.edu"
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Removed daniel@mergington.edu from Chess Club"
    }
    assert "daniel@mergington.edu" not in activities["Chess Club"]["participants"]
