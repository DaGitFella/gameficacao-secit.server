from rest_framework import serializers

from api.models.activity import Activity
from api.serializers.custom_list_serializer import CustomListSerializer
from api.serializers.stamp import StampSerializer


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['stamps_amount', 'timestamp', 'type', 'stamp']
        list_serializer_class = CustomListSerializer

    stamp = StampSerializer()

    def create_from_list(self, validated_data):
        activities = []
        for i, activity in enumerate(validated_data['activities']):
            activity.update({"event": validated_data['event']})

            stamp = next(filter(
                lambda s: s.icon == activity['stamp']['icon'],
                validated_data['created_stamps']
            ))

            activity['stamp'] = stamp

            activities.append(self.create(activity))

        return {'activities': activities}

    def create(self, validated_data):
        return self.Meta.model.objects.save_in_db(**validated_data)

    def update(self, instance, validated_data):
        raise NotImplementedError()

    def delete(self, validated_data):
        raise NotImplementedError()

    def get_all_from(self, user, should_get_created_events: bool):
        return self.Meta.model.objects.get_all_from(user, should_get_created_events)
