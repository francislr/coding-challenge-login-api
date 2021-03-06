"""therewasanattempt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.views import obtain_auth_token
from .apps.security_auth_attempt.decorators import log_success_auth_attempt as decorate_log_success_auth_attempt
from .views import AttemptEventView, AttemptEventListView

log_success_auth_attempt = decorate_log_success_auth_attempt(username_field='username', success_status_code=200)

urlpatterns = [
    path('api/login', csrf_exempt(log_success_auth_attempt(obtain_auth_token)), name='api-login'),
    path('api/attempt-event', AttemptEventView.as_view(), name='api-list-attempt-event'),
    path('', login_required(AttemptEventListView.as_view()), name='list-attempt-event'),
    path('login', LoginView.as_view(template_name='therewasanattempt/login.html'), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
]
