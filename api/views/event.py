from django.db.models import QuerySet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import api.models
from api.models.event import EventManager
from api.models.user import UserManager
from api.serializers.event import EventSerializer
from api.serializers.user import UserSerializer
import json

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

        serializer = EventSerializer(data=data)

        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        event = EventService.create(serializer)
        EventManager.save_in_db(event)

        # json_data = json.dumps(request.data, indent=4)
        # print()
        # print(json_data)
        # print()
        #
        # print(type(request.data["conquests"]))

        # copy_data = serializer.data.copy()
        # copy_data.pop("user_who_created")
        # json_data = json.dumps(copy_data, indent=4)
        # print()
        # print(json_data)
        # print(f'\'number\' in data: {"number" in copy_data}')
        # print()

        # serializer.create(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def get(request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = EventSerializer()
        should_get_created_events: bool = 'created' in request.query_params and request.query_params['created']

        if should_get_created_events and request.user.role != api.models.User.Roles.ADMIN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        query_data: QuerySet = serializer.get_all_from(request.user, should_get_created_events)
        return Response(data=list(query_data.values()), status=status.HTTP_200_OK)

    @staticmethod
    def put(request):
        raise NotImplementedError()

    @staticmethod
    def delete(request):
        raise NotImplementedError()
