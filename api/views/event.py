from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import api.models
from api.serializers.event import EventSerializer
from api.services.event import EventService


class EventView(APIView):
    @staticmethod
    def post(request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if request.user.role != api.models.User.Roles.ADMIN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()
        data.update({"user_who_created": request.user.id})

        # print('--- Incoming data in EventView ---')
        # print(data)

        serializer = EventSerializer(data=data)

        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        event = EventService.create(serializer)
        serializer = EventSerializer(event)
        print('--- Created Event in EventView ---')
        print(event)
        print()
        # print(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def get(request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = EventSerializer()
        should_get_created_events: bool = 'created' in request.query_params and request.query_params['created']

        if should_get_created_events and request.user.role != api.models.User.Roles.ADMIN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        return Response(
            data=EventService.get_all_from(request.user, should_get_created_events),
            status=status.HTTP_200_OK
        )

    @staticmethod
    def put(request):
        raise NotImplementedError()

    @staticmethod
    def delete(request):
        raise NotImplementedError()
