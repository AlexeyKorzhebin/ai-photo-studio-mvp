from backend.app.services.image_ops import deterministic_placeholder


def test_deterministic_placeholder_is_stable():
    one = deterministic_placeholder("cat astronaut", "1024x1024", "comic")
    two = deterministic_placeholder("cat astronaut", "1024x1024", "comic")
    assert one == two
