from django.urls import path, include
from .views import RoomViewSet, EventViewSet, Through_Event_User_customerViewSet
from .views import login, signin
from rest_framework import routers, serializers, viewsets

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
#router.register(r"register", signin, basename='Register')
router.register(r"Room", RoomViewSet, basename='Room')
router.register(r"Event", EventViewSet, basename='Event')
router.register(r"Through_Event_User_customer", Through_Event_User_customerViewSet, basename='Event')
#router.register(r"Pregunta", PreguntaViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("api/", include(router.urls)),
    path("api/api-token-auth", login),
    path('api/signin', signin),
]
