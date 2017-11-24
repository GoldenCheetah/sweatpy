test:
	pytest

coverage:
	coverage run --source=athletic_pandas -m pytest --
	coverage report
	coverage html

isort:
	isort --skip=venv
