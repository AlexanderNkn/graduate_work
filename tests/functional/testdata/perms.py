import pytest


@pytest.fixture
def perms_list():
    return [
        "/login",
        "/logout",
        "/film",
        "/admin",
        "/users"
        "/roles"
    ]
