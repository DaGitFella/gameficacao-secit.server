from rest_framework import serializers

from api.models.activity import Activity
from api.serializers.custom_list_serializer import CustomListSerializer
from api.serializers.stamp import StampSerializer
from api.services.activity import ActivityService


class ActivityListSerializer(CustomListSerializer):
    @staticmethod
    def validate_stamps_icons(conquests: list[dict], activities: list[dict]) -> list[dict]:
        errors = ActivityService.validate_stamps_icons(conquests, activities)
        if errors:
            raise serializers.ValidationError({"activities": errors})

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['stamps_amount', 'type', 'stamp']
        list_serializer_class = ActivityListSerializer

    stamp = StampSerializer()
