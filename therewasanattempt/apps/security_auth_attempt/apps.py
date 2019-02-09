from django.apps import AppConfig


class SecurityAuthAttemptConfig(AppConfig):
    name = 'therewasanattempt.apps.security_auth_attempt'
    verbose_name = "Authentication attempt"

    def ready(self):
        # Load signals
        from . import signals
