from django.contrib import admin
from .models import AttemptEvent

class AttemptEventAdmin(admin.ModelAdmin):
    readonly_fields = ('time_created', 'username', 'ip_address', 'user_agent', 'result')
    list_display = ('time_created', 'username', 'ip_address', 'user_agent', 'result')
    list_display_links = ('time_created', 'username', 'ip_address', 'user_agent', 'result')
    list_filter = ('result',)
    ordering = ['-time_created']

admin.site.register(AttemptEvent, AttemptEventAdmin)
