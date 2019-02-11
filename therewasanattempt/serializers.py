from rest_framework.serializers import ModelSerializer
from therewasanattempt.apps.security_auth_attempt.models import AttemptEvent

class AccountSerializer(ModelSerializer):
    class Meta:
        model = AttemptEvent
        fields = ('time_created', 'username', 'ip_address', 'user_agent', 'result')
