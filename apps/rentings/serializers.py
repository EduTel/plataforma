from .models import Room, Event, Through_Event_User_customer
from django.contrib.auth.models import User, Group
from rest_framework import routers, serializers, viewsets
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import Group, Permission

class BaseSerializer(serializers.HyperlinkedModelSerializer):
    created_at = serializers.DateTimeField(read_only=True, input_formats='%m-%Y', format='%d-%m-%Y %H:%M:%S')
    updated_at = serializers.DateTimeField(read_only=True, input_formats='%m-%Y', format='%d-%m-%Y %H:%M:%S')
    deleted = serializers.BooleanField(required=True)

class RoomSerializer(BaseSerializer):

    class Meta:
        """
        """
        model = Room
        fields = ["id", "name", "capacity", "created_at", "updated_at"]


class EventSerializer(BaseSerializer):
    obj_room = RoomSerializer(allow_null=True, required=False, read_only=True)
    id_room = serializers.PrimaryKeyRelatedField(source='obj_room',
        queryset=Room.objects.filter(deleted=False),
        required=True,
        write_only=True,
        allow_null=True)

    user = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='User-detail'  # <modelname>-detail
	)
    class Meta:
        model = Event
        fields = ["id", "name", "types", "id_room", "obj_room", "date", "user", "created_at", "updated_at"]

#class Through_Room_User_busines_Serializer(BaseSerializer):
#	obj_user_busines = serializers.PrimaryKeyRelatedField(many=False, queryset=User.objects.all())
#	obj_room = serializers.PrimaryKeyRelatedField(many=False, queryset=Room.objects.all())
#
#	class Meta:
#		model = Through_Room_User_busines
#		fields = ["id", "obj_user_busines", "obj_room", "created_at", "updated_at"]

class Through_Event_User_Serializer(BaseSerializer):
    obj_user_customer = serializers.PrimaryKeyRelatedField(many=False, queryset=User.objects.all())
    obj_event = serializers.PrimaryKeyRelatedField(many=False, queryset=Event.objects.all())

    class Meta:
        model = Through_Event_User_customer
        fields = ["id", "obj_user_customer", "obj_event", "active", "created_at", "updated_at"]

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)