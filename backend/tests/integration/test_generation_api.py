def test_generation_uses_fallback(client):
    response = client.post("/api/generation", json={"prompt": "forest fox", "size": "1024x1024"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["provider"] == "fallback"
    asset_response = client.get(f"/api/assets/{payload['asset_id']}")
    assert asset_response.status_code == 200
