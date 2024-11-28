from scrapegraph_py.exceptions import APIError


def test_api_error():
    error = APIError("Test error", status_code=400)
    assert str(error) == "[400] Test error"
    assert error.status_code == 400
    assert error.message == "Test error"


def test_api_error_without_status():
    error = APIError("Test error")
    assert str(error) == "[None] Test error"
    assert error.status_code is None
    assert error.message == "Test error"
