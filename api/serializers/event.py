from rest_framework import serializers

from api.models.event import Event
from api.serializers.activity import ActivitySerializer
from api.serializers.award import AwardSerializer
from api.serializers.conquest import ConquestSerializer
from api.serializers.user import UserSerializer
from api.services.event import EventService
from api.services.user import UserService


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'user_who_created', 'name', 'year', 'edition_number', 'conquests', 'awards', 'activities']

    conquests = ConquestSerializer(many=True)
    awards = AwardSerializer(many=True)
    activities = ActivitySerializer(many=True)
    user_who_created = UserSerializer()

    def to_internal_value(self, data):
        return {
            "name": data["name"],
            "year": data["year"],
            "edition_number": data["edition_number"],
            "user_who_created": UserService.get_from_pk(data["user_who_created"]),
            "conquests": ConquestSerializer(many=True, data=data["conquests"]),
            "awards": AwardSerializer(many=True, data=data["awards"]),
            "activities": ActivitySerializer(many=True, data=data["activities"])
        }

    @staticmethod
    def validate_conquests(conquests_data):
        EventService.raise_if_invalid_conquests(conquests_data)
        return conquests_data

    @staticmethod
    def validate_awards(awards_data):
        EventService.raise_if_invalid_awards(awards_data)
        return awards_data

    @staticmethod
    def validate_activities(activities_data):
        EventService.raise_if_invalid_activities(activities_data)
        return activities_data

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        print('\n--- representation in EventSerializer.to_representation ---')
        print(representation)

        representation["user_who_created"] = UserSerializer(instance.user_who_created).data
        return representation
