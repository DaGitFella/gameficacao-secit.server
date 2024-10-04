from rest_framework import serializers


class CustomListSerializer(serializers.ListSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __iter__(self):
        self.is_valid()
        self.generator = iter(self.validated_data)
        # print("$@$ "*5, "Passed through __iter__ in CustomListSerializer", self.is_valid(), self.errors)
        return self.generator

    def __next__(self):
        return next(self.generator)
