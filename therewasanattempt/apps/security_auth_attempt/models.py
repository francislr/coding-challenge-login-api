from django.db import models
from django.contrib.auth.models import User

# Length of the username field
USERNAME_MAX_LENGTH = User._meta.get_field(User.USERNAME_FIELD).max_length

AUTHENTICATION_RESULT_FAILURE = 'FAIL'
AUTHENTICATION_RESULT_SUCCESS = 'SUCC'
AUTHENTICATION_RESULT_BLOCKED = 'DENY'

AUTHENTICATION_RESULT = (
    (AUTHENTICATION_RESULT_FAILURE, 'Failure'),
    (AUTHENTICATION_RESULT_SUCCESS, 'Success'),
    (AUTHENTICATION_RESULT_BLOCKED, 'Blocked'),
)

class AttemptEvent(models.Model):
    """
    Authentication attempt events are created when credentials are validated through
    the authentication system.
    """
    time_created = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=USERNAME_MAX_LENGTH)
    ip_address = models.GenericIPAddressField(max_length=30)
    user_agent = models.CharField(max_length=200, null=True, blank=True)
    result = models.CharField(max_length=4, choices=AUTHENTICATION_RESULT)

    class Meta:
        verbose_name = 'Authentication attempt'
        verbose_name_plural = 'Authentication attempts'

    def __str__(self):
        return "[%s] Authentication attempt from \"%s\" using username \"%s\"" % (self.time_created, self.ip_address, self.username)

    @staticmethod
    def from_request(request):
        """
        Create a new AttemptEvent from HTTP request object
        """
        attempt_event = AttemptEvent()

        # Store User-Agent header if present
        if 'HTTP_USER_AGENT' in request.META:
            attempt_event.user_agent = request.META['HTTP_USER_AGENT']
        else:
            attempt_event.user_agent = None

        # Store IP address
        if 'REMOTE_ADDR' in request.META:
            attempt_event.ip_address = request.META['REMOTE_ADDR']
        else:
            raise RuntimeError('REMOTE_ADDR in request.META is not present')

        return attempt_event
