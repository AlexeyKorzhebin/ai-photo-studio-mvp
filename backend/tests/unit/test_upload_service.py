from io import BytesIO


def test_rejects_invalid_type(client):
    response = client.post("/api/assets/upload", files={"file": ("bad.txt", BytesIO(b"hello"), "text/plain")})
    assert response.status_code == 400
