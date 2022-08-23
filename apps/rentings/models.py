from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.contrib import admin
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.db.models import Q
from pprint import pprint
from rest_framework.decorators import api_view


# Create your models here.

class Base(models.Model):
    created_at = models.DateTimeField(verbose_name="creation date", auto_now_add=True, null=True)
    updated_at = models.DateTimeField(verbose_name="update date", auto_now=True, null=True)
    deleted = models.BooleanField(verbose_name="deleted", default=False)

    class Meta:
        abstract = True

class Room(Base):
    name = models.CharField(verbose_name="Name", max_length=150)
    capacity = models.IntegerField(verbose_name="Capacity")
    #user = models.ManyToManyField(User, blank=True, through="Through_Room_User_busines")

    """
        The business can create a room with M capacity
    """
    obj_user_busines = models.ForeignKey(User, related_name='Rooms', verbose_name="User_busines",
        on_delete=models.CASCADE,
        limit_choices_to={'groups': 2}, null=True) # Business


    def save(self, *args, **kwargs):
        """
            The business can create events for every room.
        """
        #print("args",  args)
        #print("kwargs",  kwargs)
        if 2 in list(self.obj_user_busines.groups.values_list('id', flat=True)):
            super(Room, self).save(*args, **kwargs)
        else:
            raise serializers.ValidationError("it is not a busines")

    def __str__(self):
        return str(self.pk) + "-" + str(self.name)

#class Through_Room_User_busines(Base):
#    obj_user_busines = models.ForeignKey(User, related_name='Through_Room_User_busines', verbose_name="User_busines",
#        on_delete=models.CASCADE,
#        limit_choices_to={'groups': 2}) # Business
#    obj_room = models.ForeignKey(Room, related_name='Through_Room_User_busines', verbose_name="Event", on_delete=models.CASCADE)

class Event(Base):
    class Types(models.TextChoices):
        PUBLIC = "public"
        PRIVATE = "private"

    name = models.CharField(verbose_name="Name", max_length=150)
    """
        The business can delete a room if said room does not have any events.
    """
    obj_room = models.ForeignKey(Room, related_name='Events', verbose_name="Rooms", on_delete=models.PROTECT)
    user = models.ManyToManyField(User, blank=True, through="Through_Event_User_customer")
    types = models.CharField(max_length=7, choices=Types.choices, default=Types.PUBLIC)
    date = models.DateField()
    """
        The business can create events for every room.
    """
    obj_user_busines = models.ForeignKey(User, related_name='Events', verbose_name="User_busines",
        on_delete=models.CASCADE,
        limit_choices_to={'groups': 2}, null=True) # Business

    def save(self, *args, **kwargs):
        """
            The business can create events for every room.
        """
        #print("args",  args)
        #print("kwargs",  kwargs)
        if 2 in list(self.obj_user_busines.groups.values_list('id', flat=True)):
            super(Event, self).save(*args, **kwargs)
        else:
            raise serializers.ValidationError("it is not a busines")

    @property
    def count(self):
        return Through_Event_User_customer.objects.filter(obj_event__pk=self.pk, active=True).count()

    def __str__(self):
        return str(self.pk) + "-" + str(self.name)

    """
        - For now, there is only one event per day.
    """
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["obj_room", "date"],
                name="unique__obj_room__date"
            )
        ]

class Through_Event_User_customer(Base):
    obj_user_customer = models.ForeignKey(User, related_name='Through_Event_User_customer', verbose_name="User_customer",
        on_delete=models.CASCADE,
        limit_choices_to={'groups': 1}) # Customer
    obj_event = models.ForeignKey(Event, related_name='Through_Event_User_customer', verbose_name="Event", on_delete=models.CASCADE)
    active = models.BooleanField(verbose_name="Active", default=True)

    def save(self, *args, **kwargs):
        """
            If the event is public, any customer can book a space.
            If the event is private, no one else can book a space in the roo
            If the event is private, no one else can book a space in the room.
        """
        print("===========obj_event", self.obj_event.pk)
        capacity = Event.objects.get(pk=self.obj_event.pk).obj_room.capacity
        occupation = Through_Event_User_customer.objects.filter(obj_event__pk=self.obj_event.pk, active=True).count()
        types = self.obj_event.types
        print("capacity", capacity)
        print("occupation", occupation)
        print("types", types)
        if capacity > occupation: # cuando es un update
            if self.obj_event.types == "public":
                super(Through_Event_User_customer, self).save(*args, **kwargs)
            else:
                #messages.add_message(request, messages.INFO,'event private"') 
                raise serializers.ValidationError("event private")
        else:
            #messages.add_message(request, messages.INFO,'maximun limit capacity"') 
            raise serializers.ValidationError("maximun limit capacity")
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["obj_user_customer", "obj_event", "active"],
                name="unique__obj_user_customer__obj_event__active"
            )
        ]