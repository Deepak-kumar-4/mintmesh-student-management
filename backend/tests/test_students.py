from datetime import date, timedelta


def make_student_payload(**overrides):
    payload = {
        "first_name": "Ada",
        "last_name": "Lovelace",
        "email": "ada@example.com",
        "date_of_birth": "1990-01-01",
        "enrollment_status": "active",
    }
    payload.update(overrides)
    return payload


def test_create_student_success(client):
    payload = make_student_payload()
    response = client.post("/students", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["first_name"] == payload["first_name"]
    assert data["last_name"] == payload["last_name"]
    assert data["email"] == payload["email"]
    assert data["date_of_birth"] == payload["date_of_birth"]
    assert data["enrollment_status"] == payload["enrollment_status"]


def test_create_student_invalid_email(client):
    payload = make_student_payload(email="not-an-email")
    response = client.post("/students", json=payload)

    assert response.status_code == 400


def test_create_student_future_dob(client):
    future_date = (date.today() + timedelta(days=1)).isoformat()
    payload = make_student_payload(date_of_birth=future_date)
    response = client.post("/students", json=payload)

    assert response.status_code == 400


def test_create_student_duplicate_email(client):
    payload = make_student_payload()
    first = client.post("/students", json=payload)
    assert first.status_code == 201

    second = client.post("/students", json=make_student_payload(first_name="Grace"))
    assert second.status_code == 409


def test_get_student_not_found(client):
    response = client.get("/students/99999")

    assert response.status_code == 404


def test_get_student_success(client):
    created = client.post("/students", json=make_student_payload())
    student_id = created.json()["id"]

    response = client.get(f"/students/{student_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == student_id
    assert data["email"] == make_student_payload()["email"]


def test_update_student_not_found(client):
    response = client.patch("/students/99999", json={"first_name": "Nobody"})

    assert response.status_code == 404


def test_delete_student_then_get_404(client):
    created = client.post("/students", json=make_student_payload())
    student_id = created.json()["id"]

    delete_response = client.delete(f"/students/{student_id}")
    assert delete_response.status_code == 200

    get_response = client.get(f"/students/{student_id}")
    assert get_response.status_code == 404
