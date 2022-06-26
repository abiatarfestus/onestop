DJANGO = onestop/manage.py #Reference to the DJANGO.py script

help:
	make -h

venv: #Open the virtual environment shell
	pipenv shell

check: # Check for inconsistencies using Black Formatter
	black --check --diff onestop

format: #Format code with Black and isort
	black onestop
	isort --profile black onestop

migrate: #Run migrations
	python $(DJANGO) makemigrations
	python $(DJANGO) migrate

runserver: #Run the Django localhost server
	python $(DJANGO) runserver

djangoshell: #Open the Django interactive shell
	python $(DJANGO) shell

# Pipfile.lock: Pipfile #Update Pipfile.lock file
# 	pipenv lock
