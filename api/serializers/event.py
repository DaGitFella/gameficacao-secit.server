from functools import reduce
from pprint import pprint

from django.http import QueryDict
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import PrimaryKeyRelatedField

from api.models import User
from api.models.event import Event
from api.serializers.activity import ActivitySerializer
from api.serializers.award import AwardSerializer
from api.serializers.conquest import ConquestSerializer
from api.serializers.user import UserSerializer
from api.services.event import EventService


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'user_who_created_id', 'name', 'year', 'edition_number', 'conquests', 'awards', 'activities']

    conquests = ConquestSerializer(many=True)
    awards = AwardSerializer(many=True)
    activities = ActivitySerializer(many=True)
    user_who_created_id = PrimaryKeyRelatedField(queryset=User.objects.all())

    def to_internal_value(self, data):
        print("--- data in EventSerializer.to_internal_value ---")
        print(data)
        print()

        print(self.instance)
        print()

        if self.instance is not None:
            data["user_who_created_id"] = self.instance.user_who_created.id

        try:
            internal_value = super().to_internal_value(data)
        except ValidationError as standard_exceptions:
            standard_exceptions_detail = EventService.organize_non_field_errors(standard_exceptions.detail)

            data = {
                **data,
                "conquests": ConquestSerializer(many=True, data=data["conquests"]),
                "awards": AwardSerializer(many=True, data=data["awards"]),
                "activities": ActivitySerializer(many=True, data=data["activities"])
            }

            try:
                self.validate(data)
            except ValidationError as custom_exceptions:
                print("--- standard_exceptions_detail in EventSerializer.to_internal_value ---")
                print(standard_exceptions_detail, end="\n\n")
                print("--- custom_exceptions.detail in EventSerializer.to_internal_value ---")
                print(custom_exceptions.detail, end="\n\n")

                merged_details = \
                    EventService.merge_exceptions_details(custom_exceptions.detail, standard_exceptions_detail)

                print("--- merged_details in EventSerializer.to_internal_value ---")
                print(merged_details, end="\n\n")

                raise ValidationError(merged_details)

            raise standard_exceptions

        else:
            internal_value = {
                **internal_value,
                # "user_who_created": UserService.get_from_pk(data["user_who_created_id"]),
                "conquests": ConquestSerializer(many=True, data=data["conquests"]),
                "awards": AwardSerializer(many=True, data=data["awards"]),
                "activities": ActivitySerializer(many=True, data=data["activities"])
            }

            return internal_value

        # return {
        #
        #     **super().to_internal_value(data),
        #     # "name": data["name"],
        #     # "year": data["year"],
        #     # "edition_number": data["edition_number"],
        #     "user_who_created": UserService.get_from_pk(data["user_who_created_id"]),
        #     "conquests": ConquestSerializer(many=True, data=data["conquests"]),
        #     "awards": AwardSerializer(many=True, data=data["awards"]),
        #     "activities": ActivitySerializer(many=True, data=data["activities"])
        # }

    # EventSerializer.validate doesn't run when super().to_internal_value is called;
    # Try to understand why it is happening

    def validate(self, data):
        print("\n")
        print("--- inside EventSerializer.validate ---")
        print("\n")

        serializers_keys: list[str] = ["conquests", "awards", "activities"]
        errors = []
        for key in serializers_keys:
            serializer = data[key]

            try:
                serializer.validate(serializer.initial_data)
            except serializers.ValidationError as err:
                errors.append({key: err.detail})

        try:
            data["activities"].validate_stamps_icons(
                data["conquests"].initial_data,
                data["activities"].initial_data
            )
        except serializers.ValidationError as err:
            errors.append({"activities": err.detail})

        print()
        print("--- errors before reduce in EventSerializer.validate ---")
        pprint(errors)
        print()

        if errors:
            errors = reduce(lambda e1, e2: {**e1, **e2}, errors, {})

            print("--- errors after reduce in EventSerializer.validate ---")
            pprint(errors)
            print()
            raise serializers.ValidationError(errors)

        return data

    def to_representation(self, instance):
        print('\n--- instance in EventSerializer.to_representation ---')
        print(instance)

        representation = super().to_representation(instance)

        print('\n--- representation in EventSerializer.to_representation ---')
        print(representation)

        representation.update({"user_who_created": UserSerializer(instance.user_who_created).data})
        return representation
