from src.app import activities


def test_get_activities(client):
    # Arrange: no special setup

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    body = resp.json()
    assert isinstance(body, dict)
    assert "Chess Club" in body


def test_signup_success_and_cleanup(client):
    # Arrange
    activity = "Chess Club"
    email = "tester@example.com"
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # Cleanup (Arrange for teardown)
    activities[activity]["participants"].remove(email)


def test_signup_missing_email_returns_422(client):
    # Arrange
    activity = "Chess Club"

    # Act
    resp = client.post(f"/activities/{activity}/signup")

    # Assert
    assert resp.status_code == 422


def test_signup_allows_over_capacity_behavior(client):
    # Arrange
    activity = "Tennis Club"
    max_p = activities[activity]["max_participants"]
    # fill participants up to max with distinct emails
    activities[activity]["participants"] = [f"p{i}@example.com" for i in range(max_p)]
    new_email = "overflow@example.com"
    if new_email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(new_email)

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": new_email})

    # Assert
    # Current app does not enforce capacity, so signup should succeed and be added
    assert resp.status_code == 200
    assert new_email in activities[activity]["participants"]

    # Cleanup
    activities[activity]["participants"].remove(new_email)


def test_unregister_success_and_cleanup(client):
    # Arrange
    activity = "Basketball Team"
    email = "to_remove@example.com"
    if email not in activities[activity]["participants"]:
        activities[activity]["participants"].append(email)

    # Act
    resp = client.post(f"/activities/{activity}/unregister", params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert email not in activities[activity]["participants"]


def test_unregister_not_registered_returns_400(client):
    # Arrange
    activity = "Drama Club"
    email = "nonexistent@example.com"
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Act
    resp = client.post(f"/activities/{activity}/unregister", params={"email": email})

    # Assert
    assert resp.status_code == 400


def test_unknown_activity_returns_404(client):
    # Arrange
    activity = "Nonexistent Activity"
    email = "x@example.com"

    # Act
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert resp.status_code == 404
