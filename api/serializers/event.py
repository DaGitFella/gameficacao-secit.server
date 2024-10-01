from rest_framework import serializers

from api.models.event import Event
from api.serializers.activity import ActivitySerializer
from api.serializers.award import AwardSerializer
from api.serializers.conquest import ConquestSerializer
from api.serializers.user import UserSerializer
from api.services.activity import ActivityService
from api.services.award import AwardService
from api.services.conquest import ConquestService
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

    def validate(self, data):
        serializers_to_validate = [data["conquests"], data["awards"], data["activities"]]
        for serializer in serializers_to_validate:
            serializer.validate(serializer.initial_data)

        data["activities"].validate_stamps_icons(
            data["conquests"].initial_data,
            data["activities"].initial_data
        )

        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        print('\n--- representation in EventSerializer.to_representation ---')
        print(representation)

        representation["user_who_created"] = UserSerializer(instance.user_who_created).data
        return representation
