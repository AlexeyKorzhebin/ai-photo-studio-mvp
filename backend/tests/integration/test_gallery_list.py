from io import BytesIO

from PIL import Image


def make_image(fmt: str = "PNG"):
    buffer = BytesIO()
    Image.new("RGB", (32, 32), "red").save(buffer, format=fmt)
    buffer.seek(0)
    return buffer


def test_upload_and_list_assets(client):
    image = make_image()
    upload = client.post("/api/assets/upload", files={"file": ("sample.png", image, "image/png")})
    assert upload.status_code == 201
    listing = client.get("/api/assets")
    assert listing.status_code == 200
    assert len(listing.json()["items"]) == 1
