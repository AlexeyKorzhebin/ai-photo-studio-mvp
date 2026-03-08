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


def test_list_images_search_terms_use_and_semantics(client, sample_image_bytes):
    first = client.post(
        "/api/images/upload",
        files={"file": ("alpha.png", sample_image_bytes, "image/png")},
    )
    second = client.post(
        "/api/images/upload",
        files={"file": ("beta.png", sample_image_bytes, "image/png")},
    )
    assert first.status_code == 200
    assert second.status_code == 200

    first_id = first.json()["id"]
    second_id = second.json()["id"]

    patch_first = client.patch(
        f"/api/images/{first_id}",
        json={"tags": "sunset", "notes": "beach"},
    )
    patch_second = client.patch(
        f"/api/images/{second_id}",
        json={"tags": "sunset", "notes": "mountain"},
    )
    assert patch_first.status_code == 200
    assert patch_second.status_code == 200

    listing = client.get("/api/images?search=sunset beach&sort=name&order=asc")
    assert listing.status_code == 200
    items = listing.json()["items"]
    assert len(items) == 1
    assert items[0]["id"] == first_id


def test_list_images_uses_stable_secondary_sort_by_id(client, sample_image_bytes):
    first = client.post(
        "/api/images/upload",
        files={"file": ("same.png", sample_image_bytes, "image/png")},
    )
    second = client.post(
        "/api/images/upload",
        files={"file": ("same.png", sample_image_bytes, "image/png")},
    )
    assert first.status_code == 200
    assert second.status_code == 200

    asc_listing = client.get("/api/images?sort=name&order=asc")
    desc_listing = client.get("/api/images?sort=name&order=desc")
    assert asc_listing.status_code == 200
    assert desc_listing.status_code == 200

    asc_same = [item["id"] for item in asc_listing.json()["items"] if item["filename"] == "same.png"]
    desc_same = [item["id"] for item in desc_listing.json()["items"] if item["filename"] == "same.png"]

    assert len(asc_same) >= 2
    assert asc_same[:2] == sorted(asc_same[:2])
    assert desc_same[:2] == sorted(desc_same[:2], reverse=True)


def test_ai_generate_mock(client):
    resp = client.post(
        "/api/ai/generate",
        json={"prompt": "red sunset over water", "size": "1024x1024", "provider": "gpt-image"},
    )
    assert resp.status_code == 200
    payload = resp.json()
    assert payload["image"]["source_type"] == "generated"
    assert payload["provider_used"] in {"mock", "gpt-image"}
    assert isinstance(payload["seed_hash"], str)
    assert payload["image"]["seed_hash"] == payload["seed_hash"]


def test_ai_generate_deterministic_metadata_is_stable_for_identical_normalized_input(client):
    req = {
        "prompt": "  red   sunset over  water ",
        "size": "1024x1024",
        "style": "  cinematic  ",
        "provider": "  gpt-image ",
    }

    first = client.post("/api/ai/generate", json=req)
    second = client.post("/api/ai/generate", json=req)
    assert first.status_code == 200
    assert second.status_code == 200

    first_payload = first.json()
    second_payload = second.json()
    assert first_payload["seed_hash"] == second_payload["seed_hash"]
    assert first_payload["image"]["seed_hash"] == second_payload["image"]["seed_hash"]
    assert first_payload["image"]["is_mock"] is True
    assert second_payload["image"]["is_mock"] is True
    assert first_payload["fallback_used"] is True
    assert second_payload["fallback_used"] is True


def test_ai_generate_deterministic_metadata_changes_with_input_delta(client):
    base = {
        "prompt": "red sunset over water",
        "size": "1024x1024",
        "style": "cinematic",
        "provider": "gpt-image",
    }
    changed_style = {
        "prompt": "red sunset over water",
        "size": "1024x1024",
        "style": "natural",
        "provider": "gpt-image",
    }

    base_resp = client.post("/api/ai/generate", json=base)
    changed_resp = client.post("/api/ai/generate", json=changed_style)
    assert base_resp.status_code == 200
    assert changed_resp.status_code == 200

    base_seed = base_resp.json()["seed_hash"]
    changed_seed = changed_resp.json()["seed_hash"]
    assert base_seed != changed_seed


def test_ai_generate_invalid_size_returns_422(client):
    resp = client.post(
        "/api/ai/generate",
        json={"prompt": "red sunset over water", "size": "800x600"},
    )
    assert resp.status_code == 422
    detail = resp.json()["detail"]
    assert any(item["loc"][-1] == "size" for item in detail)
