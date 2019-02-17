from .models import AttemptEvent, AUTHENTICATION_RESULT_SUCCESS

def log_success_auth_attempt(username_field='username', success_status_code=200):
    """
    Decorate a view whose return code indicates whether the successful attempt is logged.
    When the the success_status_code matches, log the successful authentication attempts
    to database.
    """
    def decorated_view(view):
        def wrap(request, *args, **kwargs):
            response = view(request, *args, **kwargs)
            if response.status_code == success_status_code and request.method == 'POST':
                attempt_event = AttemptEvent.from_request(request)
                try:
                    attempt_event.username = request.POST[username_field]
                except KeyError:
                    attempt_event.username = ''
                attempt_event.result = AUTHENTICATION_RESULT_SUCCESS
                attempt_event.save()
            return response
        return wrap
    return decorated_view
