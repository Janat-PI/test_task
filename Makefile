run:
	python manage.py runserver

migrate:
	python manage.py makemigrations bill
	python manage.py migrate

build:
	python3 -m venv venv && . venv/bin/activate
	pip install -r requirements.txt
	make migrate
	make run
