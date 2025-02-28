from django.urls import reverse
from django.contrib.admin.sites import AdminSite

import pytest

from apps.store.admin import AppAdmin, verify_apps
from apps.store.models import App


class DummyRequest:
    pass


@pytest.mark.django_db
class TestAppCreation:
    def test_app_creation_valid_data(self, authorization_api_client, user):
        """
        verifies that a valid request creates an app with the
        correct owner and an unverified status
        """
        url = reverse('app-create')
        data = {'title': 'Test App', 'description': 'Test description for the app', 'price': '9.99'}
        response = authorization_api_client.post(url, data, format='json')
        assert response.status_code == 201, f'Unexpected status code: {response.status_code}'
        app = App.objects.get(id=response.data['id'])
        assert app.title == 'Test App'
        assert app.owner == user
        # New apps should be unverified by default
        assert app.is_verified is False

    def test_app_creation_missing_title(self, authorization_api_client):
        """ensures that the endpoint returns a validation error when the required title field is missing"""
        url = reverse('app-create')
        data = {'description': 'Test description for the app', 'price': '9.99'}
        response = authorization_api_client.post(url, data, format='json')
        # Expect a validation error since 'title' is missing
        assert response.status_code == 400
        assert 'title' in response.data


@pytest.mark.django_db
class TestAdminVerification:
    def test_verify_apps_action(self, user, db):
        """
        creates an app instance, confirms its unverified state,
        runs the custom admin action, and then checks that the app
        is marked as verified
        """
        # Create an app instance for testing verification
        app_instance = App.objects.create(
            title='Test App', description='Description', price='19.99', owner=user, is_verified=False
        )
        admin_instance = AppAdmin(App, AdminSite())
        queryset = App.objects.filter(pk=app_instance.pk)
        # Ensure the app is not verified initially
        assert not app_instance.is_verified
        # Execute the custom admin action
        verify_apps(admin_instance, DummyRequest(), queryset)
        # Refresh from DB and check verification status
        app_instance.refresh_from_db()
        assert app_instance.is_verified is True
