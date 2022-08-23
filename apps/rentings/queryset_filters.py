from pprint import pprint
from .models import Room, Group, Through_Event_User_customer
from django.core import serializers
import json
from django.db.models import Q


def get_Room(p_user=None):
	return Room.objects.filter(deleted=False)

def get_Group(p_user=None):
    return Group.objects.filter(deleted=False)

#def get_Through_PermisosView_Group(p_user=None):
#    datas_Room_User_busines =  Through_Room_User_busines.objects.filter(deleted=False)
#    return datas_Room_User_busines

def get_Through_Event_User_customer(p_user=None):
    datas_Event_User_customer =  Through_Event_User_customer.objects.filter(deleted=False)
    return datas_Event_User_customer