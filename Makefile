test:
	pytest

coverage:
	coverage run --source=sweat -m pytest --
	coverage report
	coverage html

isort:
	isort --skip=venv
