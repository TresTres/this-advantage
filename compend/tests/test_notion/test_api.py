import notion.api as notion


def test_create_url_target():
    assert notion.create_url_target("foo") == "https://api.notion.com/v1/foo"