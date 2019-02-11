from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from therewasanattempt.apps.security_auth_attempt.models import AttemptEvent
from .serializers import AccountSerializer

class AttemptEventView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AccountSerializer
    queryset = AttemptEvent.objects.order_by('-time_created')[:30]
