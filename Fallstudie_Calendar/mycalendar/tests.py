from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse, resolve
from .models import Calendar, Event
from account.models import Account  # das ist ein bekanntes Problem
from .forms import CalendarForm
from .serializers import CalendarSerializer
from rest_framework.test import APITestCase
from django.utils import timezone


# Diese Klasse testet das Modell Calendar
class CalendarModelTest(TestCase):
    # Erstellt einen Benutzer und ein Kalendereintrag für Tests.
    def setUp(self):
        self.user = Account.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.calendar = Calendar.objects.create(name='Test Calendar', owner=self.user)

    # Überprüft, ob der Kalender korrekt erstellt wurde.
    def test_calendar_creation(self):
        self.assertEqual(self.calendar.name, 'Test Calendar')
        self.assertEqual(self.calendar.owner, self.user)

    # Testet, ob der Benutzer dem visible_for Feld des Kalenders hinzugefügt werden kann.
    def test_calendar_visible_for(self):
        self.calendar.visible_for.add(self.user)
        self.assertIn(self.user, self.calendar.visible_for.all())

    # Testet, ob der Benutzer dem editable_by Feld des Kalenders hinzugefügt werden kann.
    def test_calendar_editable_by(self):
        self.calendar.editable_by.add(self.user)
        self.assertIn(self.user, self.calendar.editable_by.all())


# Diese Klasse testet das Modell Event.
class EventModelTest(TestCase):
    # Erstellt einen Benutzer, einen Kalender und ein Ereignis.
    def setUp(self):
        self.user = Account.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.calendar = Calendar.objects.create(name='Test Calendar', owner=self.user)
        self.event = Event.objects.create(name='Test Event', calendar=self.calendar, start_date=timezone.now())

    # Überprüft, ob das Ereignis korrekt erstellt wurde.
    def test_event_creation(self):
        self.assertEqual(self.event.name, 'Test Event')
        self.assertEqual(self.event.calendar, self.calendar)


# Diese Klasse testet die Kalenderansichten.
class CalendarViewTest(TestCase):
    # Erstellt einen Benutzer und meldet ihn an.
    def setUp(self):
        self.client = Client()
        self.user = Account.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.client.login(username='testuser', password='password123')
        self.calendar = Calendar.objects.create(name='Test Calendar', owner=self.user)

    # Testet die Kalenderlistenansicht.
    def test_calendar_list_view(self):
        response = self.client.get(reverse('calendar_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mycalendar/calendar_list.html')

    # Testet die Kalendererstellungsansicht.
    def test_calendar_create_view(self):
        response = self.client.post(reverse('calendar_create'), {'name': 'New Calendar', 'owner': self.user.pk})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Calendar.objects.filter(name='New Calendar').exists())

    # Testet die Kalenderlöschansicht.
    def test_calendar_delete_view(self):
        response = self.client.post(reverse('calendar_delete', args=[self.calendar.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Calendar.objects.filter(pk=self.calendar.pk).exists())


# Diese Klasse testet die Ereignisansichten.
class EventViewTest(TestCase):
    # Erstellt einen Benutzer, einen Kalender und ein Ereignis und meldet den Benutzer an.
    def setUp(self):
        self.client = Client()
        self.user = Account.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.client.login(username='testuser', password='password123')
        self.calendar = Calendar.objects.create(name='Test Calendar', owner=self.user)
        self.event = Event.objects.create(name='Test Event', calendar=self.calendar, start_date=timezone.now())

    # Testet die Ereigniserstellungsansicht.
    def test_event_create_view(self):
        response = self.client.post(reverse('event_create'),
                                    {'name': 'New Event', 'calendar': self.calendar.pk, 'start_date': timezone.now()})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Event.objects.filter(name='New Event').exists())

    # Testet die Ereignislöschansicht.
    def test_event_delete_view(self):
        response = self.client.post(reverse('event_delete', args=[self.event.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Event.objects.filter(pk=self.event.pk).exists())


# Diese Klasse testet das CalendarForm Formular.
class CalendarFormTest(TestCase):
    # Erstellt einen Benutzer und Beispieldaten für das Formular.
    def setUp(self):
        self.user = Account.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.calendar_data = {
            'name': 'Test Calendar',
            'visible_for': 'test@example.com',
            'editable_by': 'test@example.com'
        }

    # Testet, ob das Formular mit gültigen Daten gültig ist.
    def test_valid_calendar_form(self):
        form = CalendarForm(data=self.calendar_data)
        self.assertTrue(form.is_valid())

    # Testet, ob das Formular mit ungültigen Daten ungültig ist.
    def test_invalid_calendar_form(self):
        form = CalendarForm(data={})
        self.assertFalse(form.is_valid())

    # Testet das Speichern des Formulars.
    def test_calendar_form_save(self):
        form = CalendarForm(data=self.calendar_data)
        form.is_valid()  # Fügen Sie dies hinzu, um cleaned_data zu erzeugen
        form.set_owner(self.user)
        calendar = form.save()
        self.assertEqual(calendar.name, 'Test Calendar')
        self.assertEqual(calendar.owner, self.user)
        self.assertIn(self.user, calendar.visible_for.all())
        self.assertIn(self.user, calendar.editable_by.all())


# Diese Klasse testet den CalendarSerializer.
class CalendarSerializerTest(APITestCase):
    # Erstellt einen Benutzer, einen Kalender und initialisiert den Serializer.
    def setUp(self):
        self.user = Account.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.calendar = Calendar.objects.create(name='Test Calendar', owner=self.user)
        self.serializer = CalendarSerializer(instance=self.calendar)


# Diese Klasse testet die URL-Auflösungen für das Account-Modul.
class AccountURLsTests(SimpleTestCase):
    # Testet die Registrierung-URL.
    def test_register_url_resolves(self):
        resolver = resolve('/account/register/')
        self.assertEqual(resolver.view_name, 'register')

    # Testet die Abmelde-URL.
    def test_logout_url_resolves(self):
        resolver = resolve('/account/logout/')
        self.assertEqual(resolver.view_name, 'logout')

    # Testet die Anmelde-URL.
    def test_login_url_resolves(self):
        resolver = resolve('/account/login/')
        self.assertEqual(resolver.view_name, 'login')