from django.db import models
from account.models import Account


# Calendar model to represent calendar instances
class Calendar(models.Model):
    calendar_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    visible_for = models.ManyToManyField(Account, related_name="visible_for")
    editable_by = models.ManyToManyField(Account, related_name="editable_by")

    def __str__(self):
        return self.name


# Event model to represent event instances
class Event(models.Model):
    TYPE_CHOICES = [
        ("AR", 'Arbeit'),
        ("FR", 'Freizeit'),
        ("PR", 'Privat'),
        ("GE", 'Geburtstag'),
        ("FE", 'Feiertag'),
        ("UR", 'Urlaub'),
        ("TE", 'Termin'),
        ("SO", 'Sonstiges'),
    ]
    event_id = models.AutoField(primary_key=True)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    event_type = models.CharField(max_length=2, choices=TYPE_CHOICES, default="FR")

    def __str__(self):
        return self.name
