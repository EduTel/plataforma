from django.shortcuts import render
from .models import Base, Room, Event, Through_Event_User_customer
from .serializers import RoomSerializer, EventSerializer, Through_Event_User_Serializer, UserLoginSerializer

from rest_framework import routers, serializers, viewsets
from rest_framework.response import Response
from rest_framework import viewsets, status
from pprint import pprint
from django.core import serializers
import json
# Create your views here.
# ViewSets define the view behavior.
from rest_framework.exceptions import APIException
from rest_framework import exceptions, status, views
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token
from rest_framework import permissions

from rest_framework.permissions import IsAuthenticated
from .queryset_filters import get_Room, get_Group, get_Through_Event_User_customer
from rest_framework.permissions import DjangoModelPermissions, DjangoObjectPermissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes as de_permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
)
from rest_framework.response import Response
from .authentication import token_expire_handler, expires_in, ExpiringTokenAuthentication

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.forms.models import model_to_dict

from rest_framework.filters import SearchFilter



@api_view(["POST"])
@de_permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated
def login(request):
    signin_serializer = UserLoginSerializer(data=request.data)
    if not signin_serializer.is_valid():
        return Response(signin_serializer.errors, status=HTTP_400_BAD_REQUEST)
    print("username", signin_serializer.data['username'])
    print("password", signin_serializer.data['password'])
    user = authenticate(username=signin_serializer.data['username'], password=signin_serializer.data['password'])
    print("user", user)
    token, _ = Token.objects.get_or_create(user=user)
    is_expired, token = token_expire_handler(token)

    return Response({
        'expires_in': expires_in(token),
        'token': token.key,
        'user': user.pk
    }, status=HTTP_200_OK)

@api_view(["POST"])
@de_permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated
def signin(request):
    msg_true = "Favor de revisar su correo electronico."
    signin_serializer = User(data=request.data)
    if not signin_serializer.is_valid():
        data = []
        print("errors", signin_serializer.errors)
        for row_data in signin_serializer.errors.get("email", []):
            if str(row_data) == "This field must be unique.":
                data.append(row_data)
                return Response({"msg": msg_true}, status=HTTP_200_OK)
        return Response(signin_serializer.errors, status=HTTP_400_BAD_REQUEST)
    else:
        signin_serializer.save()
    return Response({
        'msg': msg_true,
    }, status=HTTP_200_OK)


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.filter(deleted=False)

    authentication_classes = [ExpiringTokenAuthentication,]
    #permission_classes = [CustomDjangoModelPermissions,]

    def get_serializer_class(self):
        if (self.request.user.is_authenticated):
            return RoomSerializer
        raise exceptions.NotAuthenticated()
    
    def perform_create(self, serializer):
        #print("=================================perform_create")
        serializer.save(obj_user_busines=self.request.user)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.filter(deleted=False)

    authentication_classes = [ExpiringTokenAuthentication,]
    #permission_classes = [CustomDjangoModelPermissions,]

    def get_serializer_class(self):
        if (self.request.user.is_authenticated):
            return EventSerializer
        raise exceptions.NotAuthenticated()
    
    def perform_create(self, serializer):
        #print("=================================perform_create")
        serializer.save(obj_user_busines=self.request.user)

# Theclass Through_Room_User_businesViewSet(viewsets.ModelViewSet):
# The    queryset = Room.objects.filter(deleted=False)
# The
# The    #authentication_classes = [ExpiringTokenAuthentication,]
# The    #permission_classes = [CustomDjangoModelPermissions,]
# The
# The    def get_serializer_class(self):
# The        if (self.request.user.is_authenticated):
# The            return Through_Room_User_busines_Serializer
# The        raise exceptions.NotAuthenticated()

class Through_Event_User_customerViewSet(viewsets.ModelViewSet):
    queryset = Through_Event_User_customer.objects.filter(deleted=False)

    authentication_classes = [ExpiringTokenAuthentication,]
    #permission_classes = [CustomDjangoModelPermissions,]

    def get_serializer_class(self):
        if (self.request.user.is_authenticated):
            return Through_Event_User_Serializer
        raise exceptions.NotAuthenticated()


