from datetime import datetime, timedelta
import json
import pytz
from unittest import mock
from django.test import RequestFactory, TestCase, SimpleTestCase
from django.http import HttpRequest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.urls import reverse
from .apps.security_auth_attempt.models import (
    AttemptEvent, AUTHENTICATION_RESULT_SUCCESS, AUTHENTICATION_RESULT_FAILURE
)

class ApiAuthenticationTestCase(TestCase):
    """
    Test authentication with the API
    """
    def setUp(self):
        pass

    def _get_access_token(self, client):
        form_values = {'username': 'example', 'password': 'example'}

        try:
            # Check if user already exists
            User.objects.get(username=form_values['username'])
        except User.DoesNotExist:
            # Create default user
            User.objects.create_user(email='test@example.com', **form_values)

        response = client.post(reverse('api-login'), form_values)
        reply = json.loads(response.content)
        return reply['token']

    def test_authenticate_success(self):
        """
        Test the logging of successful authentication events with REST Framework
        """
        client = APIClient()
        AttemptEvent.objects.all().delete()

        # Authenticate and test if a token is returned
        self.assertIsInstance(self._get_access_token(client), str)

        # Check for object insertion
        #self.assertEqual(AttemptEvent.objects.count(), 1)

    def test_authenticate_fail(self):
        """
        Test the logging of failure authentication events with REST Framework
        """
        client = APIClient()
        form_values = {'username': 'dummy', 'password': 'dummy'}
        response = client.post(reverse('api-login'), form_values)
        reply = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertNotIn('token', reply)

        # Check for object insertion
        self.assertEqual(AttemptEvent.objects.count(), 1)

        # Check if result is present
        attempt_event = AttemptEvent.objects.get(username=form_values['username'])
        self.assertEqual(attempt_event.result, AUTHENTICATION_RESULT_FAILURE)

    def test_auth_attempt_list(self):
        """
        Test the authentication event api list
        """
        client = APIClient()
        token = self._get_access_token(client)
        dataset = [
            {'username': 'username1', 'ip_address': '1.0.0.0',
                'user_agent': 'dummy', 'result': AUTHENTICATION_RESULT_FAILURE},
            {'username': 'username1', 'ip_address': '1.0.0.0',
                'user_agent': 'dummy', 'result': AUTHENTICATION_RESULT_FAILURE},
            {'username': 'username1', 'ip_address': '1.0.0.0',
                'user_agent': 'dummy', 'result': AUTHENTICATION_RESULT_FAILURE},
        ]

        AttemptEvent.objects.all().delete()
        time_created = datetime(1970, 1, 1, 1, 1, 1, 1, pytz.utc)
        for row in dataset:
            with mock.patch('django.utils.timezone.now', mock.Mock(return_value=time_created)):
                AttemptEvent(**row).save()
            time_created = time_created + timedelta(hours=1)

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.get(reverse('api-list-attempt-event'))
        reply = json.loads(response.content)

        # Remove time_created field
        for row in reply:
            del row['time_created']

        self.assertEqual(dataset, reply)
