from rest_framework import serializers

from api.models import User
from api.models.event import Event
from api.serializers.award import AwardSerializer
from api.serializers.conquest import ConquestSerializer


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['user_who_created', 'name', 'year', 'edition_number', 'conquests', 'awards', 'activities']

    conquests = ConquestSerializer(many=True)

    def to_internal_value(self, data):
        # internal_data["conquests"] = ConquestSerializer(data=data["conquests"], many=True)
        # internal_data["stamps"] = StampSerializer(
        #     data=StampSerializer.get_data_from_lists(data["conquests"], internal_data["conquests"]), many=True)

        # internal_data["conquests"] = ConquestSerializer.create_serializers_from_list(data["conquests"])

        # print(internal_data['conquests'])
        # print('aqui')
        # internal_data[]

        return {
            "name": data["name"],
            "year": data["year"],
            "edition_number": data["edition_number"],
            "user_who_created": User.objects.get(id=int(data["user_who_created"])),
            "conquests": ConquestSerializer(many=True, data=data["conquests"]),
            "awards": AwardSerializer(many=True, data=data["awards"]),
            "activities": AwardSerializer(many=True, data=data["activities"])
        }

    # def create(self, validated_data) -> Event:
    #     event = self.Meta.model.objects.create(**validated_data)
    #     validated_data.update({"event": event})
    #
    #     created_entities = ConquestSerializer().create_from_list(validated_data)
    #     validated_data.update(created_entities)
    #
    #     ActivitySerializer().create_from_list(validated_data)
    #     AwardSerializer().create_from_list(validated_data)
    #
    #     return event

    def update(self, instance, validated_data):
        raise NotImplementedError()

    def delete(self, validated_data):
        raise NotImplementedError()

    def get_all_from(self, user, should_get_created_events: bool):
        return self.Meta.model.objects.get_all_from(user, should_get_created_events)

    def validate_conquests(self, conquests_data):
        for conquest_data in conquests_data:
            serializer = ConquestSerializer(data=conquest_data)
            if not serializer.is_valid():
                raise serializers.ValidationError(f"Conquest '{conquest_data}' could not be created.")

        return conquests_data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop("user_who_created")
        representation["conquests"] = list(map(lambda c: c.data, representation["conquests"]))

        return representation
