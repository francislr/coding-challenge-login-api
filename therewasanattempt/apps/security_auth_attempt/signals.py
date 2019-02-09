from django.contrib.auth.signals import user_login_failed, user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import (
    AUTHENTICATION_RESULT_FAILURE, AUTHENTICATION_RESULT_SUCCESS, AttemptEvent
)

@receiver(user_login_failed)
def log_auth_attempt_failure(credentials, request, **kwargs):
    """
    Log authentication failure events to database
    """
    attempt_event = AttemptEvent.from_request(request)
    attempt_event.username = credentials['username']
    attempt_event.result = AUTHENTICATION_RESULT_FAILURE
    attempt_event.save()

@receiver(user_logged_in)
def log_auth_attempt_success(user, request, **kwargs):
    """
    Log authentication success events to database
    """
    attempt_event = AttemptEvent.from_request(request)
    attempt_event.username = getattr(user, user.USERNAME_FIELD)
    attempt_event.result = AUTHENTICATION_RESULT_SUCCESS
    attempt_event.save()
