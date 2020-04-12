build_docker:
	docker build -t sweatpy-test .

test:
	docker run -it --rm -v ${PWD}/.tox:/src/.tox sweatpy-test tox -e py38

testall:
	docker run -it --rm --cpus="3" -v ${PWD}/.tox:/src/.tox sweatpy-test
