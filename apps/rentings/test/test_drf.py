from django.test import TestCase
from django.core import management
from django.core.management import call_command
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
from django.db import IntegrityError


# Create your tests here.
from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase
from django.test import TestCase as test_TestCase
from unittest import TestCase as unittest_TestCase
from rest_framework import status
#from .models import Task
from rest_framework.test import APIClient
from pprint import pprint
from django.contrib.auth.models import User, Group
from apps.rentings.models import Room, Event, Through_Event_User_customer
from django.test import Client
from apps.rentings.views import RoomViewSet, EventViewSet, Through_Event_User_customerViewSet
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
import json
import shutil
from pprint import pprint
from django.conf import settings


class TaskApiTests(APITestCase):
	"""
		Esta clase es para las pruebas unitarias
	"""
	client = APIClient()

	def setUp(self):
		"""
			valores de entrada para hacer pruebas unitarias
		"""
		customer = Group.objects.create(name='Customer')
		business = Group.objects.create(name='Business')
		eduardoCustomer = User.objects.create(username="eduardoCustomer", password="321Asd1_")
		juanCustomer = User.objects.create(username="juanCustomer", password="321Asd1_")
		ricardoCustomer = User.objects.create(username="ricardoCustomer", password="321Asd1_")
		pepeBusiness = User.objects.create(username="pepeBusiness", password="321Asd1_")
		customer.user_set.add(eduardoCustomer)
		customer.user_set.add(juanCustomer)
		customer.user_set.add(ricardoCustomer)
		business.user_set.add(pepeBusiness)

	def test_login_api_post_rooms(self):
		factory = APIRequestFactory()
		request_post = factory.post('/rentings/api/Room/', {"name": "room1", "capacity": 2}, format='json')
		view = RoomViewSet.as_view({'get': 'list', 'post': 'create'})
		user = User.objects.get(username='pepeBusiness')
		force_authenticate(request_post, user=user)
		response_result = view(request_post)
		self.assertEqual(
			{'name': response_result.data.get('name'), 'capacity': response_result.data.get('capacity')},
			{'name': 'room1', 'capacity': 2})
	
	def test_login_api_get_rooms(self):
		self.test_login_api_post_rooms()
		factory = APIRequestFactory()
		request_get = factory.get('/rentings/api/Room/')
		view = RoomViewSet.as_view({'get': 'list'})
		user = User.objects.get(username='pepeBusiness')
		force_authenticate(request_get, user=user)
		response_result = view(request_get)
		self.assertEqual(len(response_result.data), 1)

	def test_login_api_post_event(self):
		self.test_login_api_post_rooms()
		factory = APIRequestFactory()
		request_post = factory.post('/rentings/api/Room/',
			{'id_room': 1, 'name': 'event1', 'types': 'public', 'date': '2022-08-10'}, format='json')
		view = EventViewSet.as_view({'get': 'list', 'post': 'create'})
		user = User.objects.get(username='pepeBusiness')
		force_authenticate(request_post, user=user)
		response_result = view(request_post)
		self.assertEqual(
			{'name': response_result.data.get('name'), 'types': response_result.data.get('types'), 'date': response_result.data.get('date')},
			{'name': 'event1', 'types': 'public', 'date': '2022-08-10'})
	
	def test_login_api_post_2_event_same_time_and_room(self):
		self.test_login_api_post_rooms()
		factory = APIRequestFactory()
		request_post = factory.post('/rentings/api/Room/',
			{'id_room': 1, 'name': 'event1', 'types': 'public', 'date': '2022-08-10'}, format='json')
		request_post2 = factory.post('/rentings/api/Room/',
			{'id_room': 1, 'name': 'event2', 'types': 'public', 'date': '2022-08-10'}, format='json')
		view = EventViewSet.as_view({'get': 'list', 'post': 'create'})
		user = User.objects.get(username='pepeBusiness')
		force_authenticate(request_post, user=user)
		force_authenticate(request_post2, user=user)
		response_result1 = view(request_post)
		try:
			response_result2 = view(request_post2)
			print("response_result2.data", response_result2.data)
			raise Exception("there are a problem here")
		except IntegrityError as e:
			print("e.args", e.args)
			if 'UNIQUE constraint failed: rentings_event.obj_room_id, rentings_event.date' in e.args[0]:
				print('error1')
				self.assertEqual(
					'UNIQUE constraint failed: rentings_event.obj_room_id, rentings_event.date',
					e.args[0])
	
