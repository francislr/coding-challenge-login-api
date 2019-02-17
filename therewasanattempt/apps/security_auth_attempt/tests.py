from django.test import RequestFactory, Client, TestCase, SimpleTestCase
from django.http import HttpRequest
from .models import AttemptEvent
from .signals import log_auth_attempt_failure, log_auth_attempt_success

class AuthAttemptSignalTestCase(TestCase):
    """
    Test logging to database from signal handlers
    """
    def setUp(self):
        pass

    def test_log_auth_attempt_failure_signal(self):
        """
        Test the login fail signal
        """
        from .models import AUTHENTICATION_RESULT_FAILURE
        AttemptEvent.objects.all().delete()

        form_values = {'username': 'example'}
        request = HttpRequest()
        request.method = 'POST'
        request.POST = form_values
        request.META['HTTP_USER_AGENT'] = 'dummy'
        request.META['REMOTE_ADDR'] = '127.0.0.1'
        log_auth_attempt_failure(credentials=form_values, request=request)

        # Check for object insertion
        self.assertEqual(AttemptEvent.objects.count(), 1)

        # Check if result is present
        attempt_event = AttemptEvent.objects.get(username=form_values['username'])
        self.assertEqual(attempt_event.result, AUTHENTICATION_RESULT_FAILURE)

    def test_log_auth_attempt_success_signal(self):
        """
        Test the login success signal
        """
        from .models import AUTHENTICATION_RESULT_SUCCESS
        from django.contrib.auth.models import User
        AttemptEvent.objects.all().delete()

        user = User(username='example')

        request = HttpRequest()
        request.method = 'POST'
        request.POST = {'username': user.username}

        request.META['HTTP_USER_AGENT'] = 'dummy'
        request.META['REMOTE_ADDR'] = '127.0.0.1'
        log_auth_attempt_success(user=user, request=request)

        # Check for object insertion
        self.assertEqual(AttemptEvent.objects.count(), 1)

        # Check if result is present
        attempt_event = AttemptEvent.objects.get(username=user.username)
        self.assertEqual(attempt_event.result, AUTHENTICATION_RESULT_SUCCESS)

class AuthAttemptViewTestCase(TestCase):
    """
    Test logging to database from the usage of generic views (integration)
    """
    def setUp(self):
        self.factory = Client()

    """
    Process a username/password form using the generic login view
    """
    def _post_credential_request(self, form_values):
        from django.contrib.auth.views import LoginView
        from django.views.decorators.csrf import csrf_exempt
        request = super(Client, self.factory).request()
        request.session = self.factory.session
        # TheCSRF exempt decorator proposed by the documentation does not work because
        # generic views are decorated with many decorators. To disable CSRF check, we
        # set the csrf_processing_done property to True, but it might break in a future
        # version...
        request.csrf_processing_done = True # TODO: 
        request.method = 'POST'
        request.POST = form_values
        request.META['HTTP_USER_AGENT'] = 'dummy'
        login_view = csrf_exempt(LoginView.as_view())

        return login_view(request)

    def test_authenticate_failure(self):
        """
        Authenticate using the generic view with wrong credentials
        Test the logging of the event to database
        """
        from .models import AUTHENTICATION_RESULT_FAILURE
        AttemptEvent.objects.all().delete()

        # Post to generic login view
        form_values = {'username': 'example', 'password': 'example'}
        self._post_credential_request(form_values)

        # Check for object insertion
        self.assertEqual(AttemptEvent.objects.count(), 1)

        # Check if result is present
        attempt_event = AttemptEvent.objects.get(username=form_values['username'])
        self.assertEqual(attempt_event.result, AUTHENTICATION_RESULT_FAILURE)

    def test_authenticate_success(self):
        """
        Authenticate using the generic view with valid credentials
        Test the logging of the event to database
        """
        from .models import AUTHENTICATION_RESULT_SUCCESS
        from django.contrib.auth.models import User
        AttemptEvent.objects.all().delete()

        form_values = {'username': 'example', 'password': 'example'}
        User.objects.create_user(email='test@example.com', **form_values)

        # Post to generic login view
        self._post_credential_request(form_values)

        # Check for object insertion
        self.assertEqual(AttemptEvent.objects.count(), 1)

        # Check if result is present
        attempt_event = AttemptEvent.objects.get(username=form_values['username'])
        self.assertEqual(attempt_event.result, AUTHENTICATION_RESULT_SUCCESS)

    def test_authenticate_success_using_decorator(self):
        """
        Successfuly authenticate using a decorated view
        Test the logging of the event to database
        """
        from .models import AUTHENTICATION_RESULT_SUCCESS
        from django.http import HttpResponse
        from .decorators import log_success_auth_attempt
        AttemptEvent.objects.all().delete()

        def get_request(method, form_values):
            request = super(Client, self.factory).request()
            request.method = method
            if request.method == 'POST':
                request.POST = form_values
            return request

        @log_success_auth_attempt(username_field='username', success_status_code=200)
        def success_view(request):
            # 200 = OK
            return HttpResponse(status=200)

        @log_success_auth_attempt(username_field='username', success_status_code=200)
        def fail_view(request):
            # 403 = Forbidden
            return HttpResponse(status=403)

        # GET requests must not log
        success_view(get_request('GET', {'username': 'ABC'}))
        self.assertEqual(AttemptEvent.objects.count(), 0)

        # POST requests with '200' response code must log to database
        success_view(get_request('POST', {'username': 'ABC'}))
        self.assertEqual(AttemptEvent.objects.count(), 1)

        # POST requests with '203' response code must not log to database
        fail_view(get_request('POST', {'username': 'ABC'}))
        self.assertEqual(AttemptEvent.objects.count(), 1)

        # POST requests with '200' response code without username field
        # must log empty username to database
        success_view(get_request('POST', {}))
        self.assertEqual(AttemptEvent.objects.count(), 2)
        self.assertEqual(AttemptEvent.objects.filter(username='').count(), 1)

class AuthAttemptTestCase(TestCase):
    def setUp(self):
        pass

    def test_creation_from_request_with_user_agent(self):
        form_values = {'username': 'example', 'password': 'example'}
        request = HttpRequest()
        request.method = 'POST'
        request.POST = form_values

        # With User-Agent and IP Address
        request.META['HTTP_USER_AGENT'] = 'dummy'
        request.META['REMOTE_ADDR'] = '127.0.0.1'

        attempt_event = AttemptEvent.from_request(request)

        self.assertEqual(attempt_event.user_agent, request.META['HTTP_USER_AGENT'])
        self.assertEqual(attempt_event.ip_address, request.META['REMOTE_ADDR'])

    def test_creation_from_request_without_user_agent(self):
        form_values = {'username': 'example', 'password': 'example'}
        request = HttpRequest()
        request.method = 'POST'
        request.POST = form_values

        # Without User-Agent and with IP Address
        try:
            del request.META['HTTP_USER_AGENT']
        except KeyError:
            pass
        request.META['REMOTE_ADDR'] = '127.0.0.1'

        attempt_event = AttemptEvent.from_request(request)

        self.assertEqual(attempt_event.user_agent, None)
        self.assertEqual(attempt_event.ip_address, request.META['REMOTE_ADDR'])

    def test_creation_from_request_without_ip_addr(self):
        """
        Note: Creation without IP Address must fail because it is most likely due to misconfig.
        """
        form_values = {'username': 'example', 'password': 'example'}
        request = HttpRequest()
        request.method = 'POST'
        request.POST = form_values

        try:
            del request.META['REMOTE_ADDR']
        except KeyError:
            pass

        with self.assertRaises(RuntimeError):
            attempt_event = AttemptEvent.from_request(request)
