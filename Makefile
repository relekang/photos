PIP=venv/bin/pip
MANAGE=venv/bin/python manage.py

setup: venv photos/settings/local.py
	${PIP} install -r requirements/dev.txt
	${MANAGE} migrate

run:
	${MANAGE} runserver 0.0.0.0:8000

production: venv photos/settings/local.py
	${PIP} install -r requirements/prod.txt
	${MANAGE} migrate
	bower install
	${MANAGE} collectstatic --noinput
	sudo supervisorctl restart photos-prod

deploy:
	${PIP} install -r requirements/prod.txt
	${MANAGE} migrate
	${MANAGE} collectstatic --noinput
	sudo supervisorctl restart photos-prod

clean:
	find . -name "*.pyc" -exec rm -rf {} \;

venv:
	virtualenv venv -p `which python3`

photos/settings/local.py:
	touch photos/settings/local.py

.PHONY: setup run clean production
