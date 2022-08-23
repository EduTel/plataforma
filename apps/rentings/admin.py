from django.contrib import admin

from .models import Room, Event, Through_Event_User_customer

class admin_Room(admin.ModelAdmin):
    list_display = [field.name for field in Room._meta.fields]

class admin_Event(admin.ModelAdmin):
    list_display = [field.name for field in Event._meta.fields]

#class admin_Through_Room_User_busines(admin.ModelAdmin):
#    list_display = [field.name for field in Through_Room_User_busines._meta.fields]

class admin_Through_Event_User_customer(admin.ModelAdmin):
    list_display = [field.name for field in Through_Event_User_customer._meta.fields]

# Register your models here.

admin.site.register(Room, admin_Room)
admin.site.register(Event, admin_Event)
#admin.site.register(Through_Room_User_busines, admin_Through_Room_User_busines)
admin.site.register(Through_Event_User_customer, admin_Through_Event_User_customer)