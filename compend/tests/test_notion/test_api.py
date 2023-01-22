from unittest.mock import patch

import pytest
import notion.api as notion


def test_create_url_target():
    assert notion.create_url_target("foo") == "https://api.notion.com/v1/foo"


class TestUnwrapHTTPResponse:
    def test_unwrap_ok_response(self, fake_http_response):
        fake_http_response.status = 210
        fake_http_response.data = '{"foo" : "bar"}'
        data = notion.unwrap_HTTP_response(fake_http_response)
        assert data == {"foo": "bar"}

    def test_unwrap_bad_response(self, fake_http_response):
        fake_http_response.status = 410
        fake_http_response.reason = "Failed"
        fake_http_response.data = '{"message" : "Unauthorized"}'
        with pytest.raises(notion.FailedRequestException) as e:
            notion.unwrap_HTTP_response(fake_http_response)
        assert str(e.value) == "Failed: Unauthorized"
