from django.contrib.auth import get_user_model

import pytest
from django_redis import get_redis_connection
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture(scope='session')
def user_credential_data():
    return {'username': 'test_user', 'email': 'user@mail.com', 'password': 'password'}


@pytest.fixture
def user(user_credential_data):
    return User.objects.create_user(**user_credential_data)


@pytest.fixture
def get_authorization_api_client(api_client):
    def _func(user):
        api_client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {RefreshToken.for_user(user).access_token.__str__()}',
        )
        return api_client

    return _func


@pytest.fixture
def authorization_api_client(get_authorization_api_client, user):
    return get_authorization_api_client(user)


@pytest.fixture(scope='session')
def cache_flusher():
    return get_redis_connection('default').flushall


@pytest.fixture(autouse=True)
def _flush_cache(cache_flusher):
    cache_flusher()
