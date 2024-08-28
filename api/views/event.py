from django.db.models import QuerySet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import api.models
from api.serializers.event import EventSerializer


class EventView(APIView):
    @staticmethod
    def post(request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if request.user.role != api.models.User.Roles.ADMIN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()
        data.update({"user", request.user})

        serializer = EventSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.create(serializer.validated_data)

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
