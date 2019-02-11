from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.views.generic import ListView
from therewasanattempt.apps.security_auth_attempt.models import AttemptEvent
from .serializers import AccountSerializer

class AttemptEventView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AccountSerializer
    queryset = AttemptEvent.objects.order_by('-time_created')[:30]

class AttemptEventListView(ListView):
    template_name = 'therewasanattempt/attempt-event-list.html'
    model = AttemptEvent
    queryset = AttemptEvent.objects.order_by('-time_created')[:30]
