from rest_framework import serializers

from api.models.award import Award
from api.models.event import Event
from api.serializers.activity import ActivitySerializer
from api.serializers.award import AwardSerializer
from api.serializers.conquest import ConquestSerializer
from api.serializers.stamp import StampSerializer


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['number', 'year', 'edition_number']

    def create(self, validated_data) -> Event:
        event = self.Meta.model.objects.create(**validated_data)
        validated_data.update({"event": event})

        created_entities = ConquestSerializer().create_from_list(validated_data)
        validated_data.update(created_entities)

        ActivitySerializer().create_from_list(validated_data)
        AwardSerializer().create_from_list(validated_data)

        return event

    def update(self, instance, validated_data):
        raise NotImplementedError()

    def delete(self, validated_data):
        raise NotImplementedError()

    def get_all_from(self, user, should_get_created_events: bool):
        return self.Meta.model.objects.get_all_from(user, should_get_created_events)
