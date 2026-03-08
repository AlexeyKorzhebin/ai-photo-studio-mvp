def test_health(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_upload_and_list(client, sample_image_bytes):
    upload = client.post(
        "/api/images/upload",
        files={"file": ("test.png", sample_image_bytes, "image/png")},
    )
    assert upload.status_code == 200
    created = upload.json()
    assert created["filename"] == "test.png"

    listing = client.get("/api/images?search=test&sort=name&order=asc")
    assert listing.status_code == 200
    items = listing.json()["items"]
    assert len(items) >= 1


def test_ai_generate_mock(client):
    resp = client.post(
        "/api/ai/generate",
        json={"prompt": "red sunset over water", "size": "1024x1024", "provider": "gpt-image"},
    )
    assert resp.status_code == 200
    payload = resp.json()
    assert payload["image"]["source_type"] == "generated"
    assert payload["provider_used"] in {"mock", "gpt-image"}


def test_ai_generate_invalid_size_returns_422(client):
    resp = client.post(
        "/api/ai/generate",
        json={"prompt": "red sunset over water", "size": "800x600"},
    )
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert any(item["loc"][-1] == "size" for item in detail)
