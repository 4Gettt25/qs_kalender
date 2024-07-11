from rest_framework import serializers
from mycalendar.models import Calendar, Event


# Serializer for the Calendar model
class CalendarSerializer(serializers.ModelSerializer):
    visible_for = serializers.SerializerMethodField("get_visible_for")
    editable_by = serializers.SerializerMethodField("get_editable_by")

    # Method to get visible_for field as a string
    def get_visible_for(self, obj):
        return "; ".join(obj.visible_for.all().values_list('email', flat=True))

    # Method to get editable_by field as a string
    def get_editable_by(self, obj):
        return "; ".join(obj.editable_by.all().values_list('email', flat=True))

    class Meta:
        model = Calendar  # Specifies the model to be used
        exclude = ("owner",)  # Fields to be excluded from the serializer


# Serializer for the Event model
class EventSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField("get_title")
    start = serializers.SerializerMethodField("get_start")
    end = serializers.SerializerMethodField("get_end")
    icon = serializers.SerializerMethodField("get_icon")

    # Method to get icon based on event_type
    def get_icon(self, obj):
        if obj.event_type == "AR":
            return "briefcase"
        else:
            return "tree"

    # Method to get title field
    def get_title(self, obj):
        return obj.name

    # Method to get start date
    def get_start(self, obj):
        return obj.start_date

    # Method to get end date
    def get_end(self, obj):
        return obj.end_date

    class Meta:
        model = Event  # Specifies the model to be used
        fields = ("title", "start", "end", "icon", "event_id", "event_type")  # Fields to be included in the serializer
