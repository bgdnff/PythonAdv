import pytest
from actions import resolve
from echo.controllers import get_echo


@pytest.fixture()
def expected_echo():
    return get_echo


def test_echo_resolve(expected_echo):
    assert resolve('echo') == expected_echo
