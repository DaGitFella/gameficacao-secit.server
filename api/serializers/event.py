from rest_framework import serializers

from api.models import User
from api.models.event import Event
from api.serializers.award import AwardSerializer
from api.serializers.conquest import ConquestSerializer
from api.serializers.user import UserSerializer
from api.services.event import EventService
from api.services.user import UserService


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['user_who_created', 'name', 'year', 'edition_number', 'conquests', 'awards', 'activities']

    conquests = ConquestSerializer(many=True)
    awards = AwardSerializer(many=True)
    activities = ConquestSerializer(many=True)
    user_who_created = UserSerializer()

    def to_internal_value(self, data):
        return {
            "name": data["name"],
            "year": data["year"],
            "edition_number": data["edition_number"],
            "user_who_created": UserService.get_from_pk(data["user_who_created"]),
            "conquests": ConquestSerializer(many=True, data=data["conquests"]),
            "awards": AwardSerializer(many=True, data=data["awards"]),
            "activities": AwardSerializer(many=True, data=data["activities"])
        }

    def update(self, instance, validated_data):
        raise NotImplementedError()

    def delete(self, validated_data):
        raise NotImplementedError()

    def get_all_from(self, user, should_get_created_events: bool):
        return self.Meta.model.objects.get_all_from(user, should_get_created_events)

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
        # instance['conquests'] = [instance['conquests']]
        # instance['awards'] = [instance['awards']]
        # instance['activities'] = [instance['activities']]

        # print(instance['conquests'])

        representation = super().to_representation(instance)
        # representation["user_who_created"] = UserSerializer(representation["user_who_created"])

        representation["user_who_created"] = instance['user_who_created']
        # print(instance['user_who_created'])

        # representation["conquests"] = list(map(lambda c: c.data, representation["conquests"]))

        return representation
