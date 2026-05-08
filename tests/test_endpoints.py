from src.app import activities


def test_root_redirects_to_static_index(client) -> None:
    response = client.get("/", follow_redirects=False)

    assert response.status_code in (302, 307)
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_payload_and_no_store_cache(client) -> None:
    response = client.get("/activities")

    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"
    assert response.json() == activities


def test_signup_adds_participant(client) -> None:
    activity_name = "Debate Club"
    email = "new.student@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {email} for {activity_name}"
    }
    assert email in activities[activity_name]["participants"]


def test_remove_participant_succeeds(client) -> None:
    activity_name = "Basketball Team"
    email = "alex@mergington.edu"

    response = client.post(f"/activities/{activity_name}/remove", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Removed {email} from {activity_name}"
    }
    assert email not in activities[activity_name]["participants"]
