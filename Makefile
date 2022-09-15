run:
	python manage.py runserver

migrate:
	python manage.py makemigrations bill
	python manage.py migrate