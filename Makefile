test:
	python -m unittest discover tests ${ARGS}

coverage:
	coverage run --source=athletic_pandas -m unittest discover tests
	coverage report
	coverage html

isort:
	isort --skip=venv
