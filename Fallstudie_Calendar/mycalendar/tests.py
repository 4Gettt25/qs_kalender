from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse, resolve
from .models import Calendar, Event
from account.models import Account
from .forms import CalendarForm
from .serializers import CalendarSerializer
from rest_framework.test import APITestCase
from django.utils import timezone

class CalendarModelTest(TestCase):
    def setUp(self):
        self.user = Account.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.calendar = Calendar.objects.create(name='Test Calendar', owner=self.user)

    def test_calendar_creation(self):
        self.assertEqual(self.calendar.name, 'Test Calendar')
        self.assertEqual(self.calendar.owner, self.user)

    def test_calendar_visible_for(self):
        self.calendar.visible_for.add(self.user)
        self.assertIn(self.user, self.calendar.visible_for.all())

    def test_calendar_editable_by(self):
        self.calendar.editable_by.add(self.user)
        self.assertIn(self.user, self.calendar.editable_by.all())

class EventModelTest(TestCase):
    def setUp(self):
        self.user = Account.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.calendar = Calendar.objects.create(name='Test Calendar', owner=self.user)
        self.event = Event.objects.create(name='Test Event', calendar=self.calendar, start_date=timezone.now())

    def test_event_creation(self):
        self.assertEqual(self.event.name, 'Test Event')
        self.assertEqual(self.event.calendar, self.calendar)

class CalendarViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Account.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.client.login(username='testuser', password='password123')
        self.calendar = Calendar.objects.create(name='Test Calendar', owner=self.user)

    def test_calendar_list_view(self):
        response = self.client.get(reverse('calendar_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mycalendar/calendar_list.html')

    def test_calendar_create_view(self):
        response = self.client.post(reverse('calendar_create'), {'name': 'New Calendar', 'owner': self.user.pk})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Calendar.objects.filter(name='New Calendar').exists())

    def test_calendar_delete_view(self):
        response = self.client.post(reverse('calendar_delete', args=[self.calendar.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Calendar.objects.filter(pk=self.calendar.pk).exists())

class EventViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Account.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.client.login(username='testuser', password='password123')
        self.calendar = Calendar.objects.create(name='Test Calendar', owner=self.user)
        self.event = Event.objects.create(name='Test Event', calendar=self.calendar, start_date=timezone.now())

    def test_event_create_view(self):
        response = self.client.post(reverse('event_create'), {'name': 'New Event', 'calendar': self.calendar.pk, 'start_date': timezone.now()})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Event.objects.filter(name='New Event').exists())

    def test_event_delete_view(self):
        response = self.client.post(reverse('event_delete', args=[self.event.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Event.objects.filter(pk=self.event.pk).exists())

class CalendarFormTest(TestCase):
    def setUp(self):
        self.user = Account.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.calendar_data = {
            'name': 'Test Calendar',
            'visible_for': 'test@example.com',
            'editable_by': 'test@example.com'
        }

    def test_valid_calendar_form(self):
        form = CalendarForm(data=self.calendar_data)
        self.assertTrue(form.is_valid())

    def test_invalid_calendar_form(self):
        form = CalendarForm(data={})
        self.assertFalse(form.is_valid())

    def test_calendar_form_save(self):
        form = CalendarForm(data=self.calendar_data)
        form.is_valid()  # Fügen Sie dies hinzu, um cleaned_data zu erzeugen
        form.set_owner(self.user)
        calendar = form.save()
        self.assertEqual(calendar.name, 'Test Calendar')
        self.assertEqual(calendar.owner, self.user)
        self.assertIn(self.user, calendar.visible_for.all())
        self.assertIn(self.user, calendar.editable_by.all())

class CalendarSerializerTest(APITestCase):
    def setUp(self):
        self.user = Account.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.calendar = Calendar.objects.create(name='Test Calendar', owner=self.user)
        self.serializer = CalendarSerializer(instance=self.calendar)

class AccountURLsTests(SimpleTestCase):

    def test_register_url_resolves(self):
        resolver = resolve('/account/register/')
        self.assertEqual(resolver.view_name, 'register')

    def test_logout_url_resolves(self):
        resolver = resolve('/account/logout/')
        self.assertEqual(resolver.view_name, 'logout')

    def test_login_url_resolves(self):
        resolver = resolve('/account/login/')
        self.assertEqual(resolver.view_name, 'login')