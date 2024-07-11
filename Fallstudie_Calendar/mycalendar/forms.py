# -*- coding: utf-8 -*-
from django import forms
from mycalendar.models import Calendar, Event
from account.models import Account
from django.db.models import Q


# Form for creating and editing Calendar instances
class CalendarForm(forms.ModelForm):
    visible_for = forms.CharField(required=False)
    editable_by = forms.CharField(required=False)

    class Meta:
        model = Calendar  # Specifies the model to be used
        exclude = ("owner", "visible_for", "editable_by")  # Fields to be excluded from the form

    # Method to set the owner of the calendar
    def set_owner(self, user):
        calendar = self.instance
        calendar.owner_id = user.pk
        self.instance = calendar

    # Method to save the calendar instance
    def save(self, commit=True):
        calendar = self.instance
        calendar.save()

        # Add users to visible_for and editable_by fields based on emails
        for email in self.cleaned_data["visible_for"].split(";"):
            if Account.objects.filter(email=email).exists():
                user = Account.objects.filter(email=email).get()
                calendar.visible_for.add(user.pk)
        for email in self.cleaned_data["editable_by"].split(";"):
            if Account.objects.filter(email=email).exists():
                user = Account.objects.filter(email=email).get()
                calendar.editable_by.add(user.pk)

        if commit:
            calendar.save()

        return calendar


# Helper function to get calendars for a user
def get_calendars(user_id):
    calendars = Calendar.objects.filter(Q(owner=user_id) | Q(editable_by=user_id))
    choices = []
    for calendar in calendars:
        choices.append((calendar.pk, calendar.name))
    return choices


# Form for editing Calendar instances
class CalendarEditForm(CalendarForm):
    visible_for = forms.CharField(required=False)
    editable_by = forms.CharField(required=False)
    calendar_id = forms.CharField(required=True)

    class Meta:
        model = Calendar  # Specifies the model to be used
        exclude = ("visible_for", "editable_by",)  # Fields to be excluded from the form

    def __init__(self, *args, **kwargs):
        super(CalendarEditForm, self).__init__(*args, **kwargs)
        if self.initial:
            self.fields["calendars"] = forms.ChoiceField(choices=get_calendars(self.initial["user_id"]), required=True)

    # Method to save the edited calendar instance
    def save(self, commit=True):
        calendar = Calendar.objects.get(calendar_id=self.cleaned_data["calendar_id"])
        calendar.name = self.cleaned_data["name"]
        calendar.editable_by.clear()
        calendar.visible_for.clear()

        # Update visible_for and editable_by fields
        for email in self.cleaned_data["visible_for"].split(";"):
            if Account.objects.filter(email=email).exists():
                user = Account.objects.filter(email=email).get()
                calendar.visible_for.add(user.pk)
        for email in self.cleaned_data["editable_by"].split(";"):
            if Account.objects.filter(email=email).exists():
                user = Account.objects.filter(email=email).get()
                calendar.editable_by.add(user.pk)

        if commit:
            calendar.save()

        return calendar


# Form for creating Event instances
class EventCreateForm(forms.ModelForm):
    start_date = forms.DateTimeField(input_formats=["%d.%m.%Y %H:%M"], required=True)
    end_date = forms.DateTimeField(input_formats=["%d.%m.%Y %H:%M"], required=False)

    # Method to set the calendar for the event
    def set_calendar(self, calendar_id):
        event = self.instance
        event.calendar_id = calendar_id
        self.instance = event

    class Meta:
        model = Event  # Specifies the model to be used
        exclude = ('calendar',)  # Fields to be excluded from the form


# Form for editing Event instances
class EventEditForm(forms.ModelForm):
    start_date = forms.DateTimeField(input_formats=["%d.%m.%Y %H:%M"], required=True)
    end_date = forms.DateTimeField(input_formats=["%d.%m.%Y %H:%M"], required=False)
    event_id = forms.CharField(required=True)

    # Method to save the edited event instance
    def save(self, commit=True):
        event = Event.objects.get(event_id=self.cleaned_data["event_id"])
        event.name = self.cleaned_data["name"]
        event.start_date = self.cleaned_data["start_date"]
        event.end_date = self.cleaned_data["end_date"]
        event.event_type = self.cleaned_data["event_type"]
        if commit:
            event.save()

        return event

    class Meta:
        model = Event  # Specifies the model to be used
        exclude = ("calendar",)  # Fields to be excluded from the form
