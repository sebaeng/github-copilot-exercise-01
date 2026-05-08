from src.app import activities


def test_signup_nonexistent_activity_returns_404(client) -> None:
    response = client.post(
        "/activities/DoesNotExist/signup", params={"email": "student@mergington.edu"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_duplicate_participant_returns_400(client) -> None:
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up"}


def test_remove_nonexistent_activity_returns_404(client) -> None:
    response = client.post(
        "/activities/DoesNotExist/remove", params={"email": "student@mergington.edu"}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_remove_missing_participant_returns_404(client) -> None:
    response = client.post(
        "/activities/Programming Class/remove",
        params={"email": "missing.student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found"}


def test_signup_empty_email_is_currently_accepted(client) -> None:
    activity_name = "Art Studio"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": ""})

    assert response.status_code == 200
    assert "" in activities[activity_name]["participants"]
