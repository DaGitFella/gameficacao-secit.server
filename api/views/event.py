from django.db.models import QuerySet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import api.models
from api.serializers.event import EventSerializer


class EventView(APIView):
    @staticmethod
    def post(request):
        raise NotImplementedError()

    @staticmethod
    def get(request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if request.user.role != api.models.User.Roles.ADMIN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = EventSerializer()
        should_get_created_events: bool = 'created' in request.query_params and request.query_params['created']
        query_data: QuerySet = serializer.get_all_from(request.user, should_get_created_events)
        return Response(data=list(query_data.values()), status=status.HTTP_200_OK)

    @staticmethod
    def put(request):
        raise NotImplementedError()

    @staticmethod
    def delete(request):
        raise NotImplementedError()
