migrate:
	python3 manage.py makemigrations && python3 manage.py migrate
run:
	python3 manage.py runserver
inspect:
	python3 manage.py inspectdb > models.py
freeze:
	pip3 freeze > requirements.txt
check:
	python3 manage.py check
run_gunicorn:
	gunicorn --bind 0.0.0.0:8000 rdc_app.wsgi
