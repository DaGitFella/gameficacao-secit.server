from rest_framework import serializers

from api.models.conquest import Conquest
from api.models.event import Event
from api.serializers.activity import ActivitySerializer
from api.serializers.award import AwardSerializer
from api.serializers.conquest import ConquestSerializer


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['user_who_created', 'name', 'year', 'edition_number', 'conquests']

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

    def validate_conquests(self, conquests_data):
        conquests = []

        for conquest_data in conquests_data:
            try:
                conquests.append(Conquest.objects.create(**conquest_data))
            except:
                raise serializers.ValidationError(f"Conquest '{conquest_data}' could not be created.")

        self.instance.conquests.set(conquests)

        return conquests
