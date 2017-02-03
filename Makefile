test:
	coverage run --source=athletic_pandas -m unittest discover tests -v
	coverage report
