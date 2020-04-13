build_docker:
	docker build -t sweatpy-test .

build_test:
	docker-compose -f docker/docker-compose.test.yml build

test: build_test
	docker-compose -f docker/docker-compose.test.yml run sweatpy tox -e py38

testall:
	docker-compose -f docker/docker-compose.test.yml run sweatpy
