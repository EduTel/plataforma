examples:

## login
``
curl --location --request POST 'http://127.0.0.1:8080/rentings/api/api-token-auth' \
--form 'username="pepeBusiness"' \
--form 'password="321Asd1_"'
``

## post Room
``
	curl --location --request POST 'http://127.0.0.1:8080/rentings/api/Room/' \
--header 'Authorization: token c3e266c7970c57c865f4fd4e92ecd9ff2fc26520' \
--form 'name="room1"' \
--form 'capacity="1"'
``

## post Event
``
curl --location --request POST 'http://127.0.0.1:8080/rentings/api/Event/' \
--header 'Authorization: token c3e266c7970c57c865f4fd4e92ecd9ff2fc26520' \
--form 'id_room="8"' \
--form 'name="event1"' \
--form 'types="public"' \
--form 'date="2022-08-10"'
``  
## test
you could execute the test with
``python manage.py test``

# superuser
```json
{
	user: edutel,
	password: 12345678
}
```

# other user
```json
{
	{
		'user': 'eduardoCustomer',
		'password': '321Asd1_'
	},
	{
		'user': 'pepeBusiness',
		'password': '321Asd1_'
	},
	{
		'user': 'juanCustomer',
		'password': '321Asd1_'
	},
	{
		'user': 'ricardoCustomer',
		'password': '321Asd1_'
	}
}
```





python manage.py createsuperuser
python manage.py runserver 8080
python manage.py migrate
python manage.py makemigrations


from apps.rentings.models import Event, Through_Event_User_customer

.
