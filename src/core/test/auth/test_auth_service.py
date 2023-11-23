from core.auth.services import AuthService
from core.user.constants import UserRole
from core.user.models import UserDomain
import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_auth_service() -> AuthService:
    return AuthService(
        MagicMock(),
        MagicMock()
    )


def test__auth_service__login__success(mock_auth_service):
    username = "luthfi"
    password = "hariz"

    mock_auth_service.user_accessor.get_by_username.return_value = (
        UserDomain(
            id=5,
            username="luthfi",
            password="hariz",
            email="dummy",
            role=UserRole.JOB_SEEKER
        )
    )

    mock_auth_service.hashing_provider.check_hash.return_value = True

    result = mock_auth_service.login(username=username, password=password)

    assert result
    assert result['id'] == 5
    assert result['username'] == 'luthfi'
    assert result['token']


def test__auth_service__login__password_unmatch(mock_auth_service):
    username = "luthfi"
    password = "hariz"

    mock_auth_service.user_accessor.get_by_username.return_value = (
        UserDomain(
            id=5,
            username="luthfi",
            password="hariz",
            email="dummy",
            role=UserRole.JOB_SEEKER
        )
    )

    mock_auth_service.hashing_provider.check_hash.return_value = False

    result = mock_auth_service.login(username=username, password=password)

    assert result is None


def test__auth_service__login__user_not_found(mock_auth_service):
    username = "luthfi"
    password = "hariz"

    mock_auth_service.user_accessor.get_by_username.return_value = None

    result = mock_auth_service.login(username=username, password=password)

    assert result is None