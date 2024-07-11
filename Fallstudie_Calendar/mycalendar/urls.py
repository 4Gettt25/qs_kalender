def some_function():
    """
    URL configuration for Fallstudie_Calendar project.

    The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/

    Examples:

    Function views:

    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')

    Class-based views:

    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')

    Including another URLconf:

    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
    """
    pass

from django.urls import path
from . import views

urlpatterns = [
    path('calendar/create/', views.CalendarCreateView.as_view(), name='calendar_create'),
    path('calendar/delete/<int:pk>/', views.CalendarDeleteView.as_view(), name='calendar_delete'),
    path('calendar/', views.CalendarListView.as_view(), name='calendar_list'),
    path('event/create/', views.EventCreateView.as_view(), name='event_create'),
    path('event/delete/<int:pk>/', views.EventDeleteView.as_view(), name='event_delete'),
]
