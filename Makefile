.PHONY: build_docker build_test test testall docs

build_docker:
	docker build -t sweatpy-test .

test:
	docker-compose -f docker/docker-compose.test.yml build
	docker-compose -f docker/docker-compose.test.yml run sweatpy tox -e py38

lint:
	docker-compose -f docker/docker-compose.lint.yml build
	docker-compose -f docker/docker-compose.lint.yml run sweatpy

testall:
	docker-compose -f docker/docker-compose.test.yml build
	docker-compose -f docker/docker-compose.test.yml run sweatpy

docs:
	docker run --rm -it -p 8000:8000 -v ${PWD}/docs:/docs squidfunk/mkdocs-material
