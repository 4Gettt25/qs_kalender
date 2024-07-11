from django.contrib import admin
from mycalendar.models import Calendar, Event

# Registering the Calendar and Event models with the Django admin site
admin.site.register(Calendar)
admin.site.register(Event)
