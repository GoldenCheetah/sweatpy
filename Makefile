build_docker:
	docker build -t sweatpy-test .

test:
	docker run -it --rm -v ${PWD}/.tox:/src/.tox sweatpy-test tox -e py38

testall:
	docker run -it --rm --cpus="3" -v ${PWD}/.tox:/src/.tox sweatpy-test

build: venv
	pipenv run python setup.py sdist bdist_wheel

test_publish: venv build
	pipenv run twine upload --repository-url https://test.pypi.org/legacy/ dist/*

publish: venv build
	pipenv run twine upload dist/*
