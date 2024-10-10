from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import user, event

urlpatterns = [
    path('users', user.UserView.as_view()),
    path('users/set_role', user.set_role),
    path('events', event.EventView.as_view()),
    path('events/<int:pk>', event.EventUpdateDeleteView.as_view()),
    path('token', TokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
]
