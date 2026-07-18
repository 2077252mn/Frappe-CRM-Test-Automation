import pytest
from automation.utils.api_client import FrappeAPI


api = FrappeAPI()


@pytest.mark.parametrize(
    "username,password,expect",
    [
        ("Administrator", "admin", True),
        ("Administrator", "123456", False),
        ("test001", "admin", False),
        ("", "admin", False),
        ("Administrator", "", False)
    ]
)
def test_login(username, password, expect):

    response = api.login(
        username,
        password
    )

    if expect:

        assert response.status_code == 200

        data = response.json()

        assert data["message"] == "Logged In"

    else:

        assert "Logged In" not in response.text