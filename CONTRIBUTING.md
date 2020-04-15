(This document is very much inspired by opensource.guide's [CONTRIBUTING.md](https://github.com/github/opensource.guide/blob/master/CONTRIBUTING.md))
# Contributing to Sweatpy

Thanks for checking out Sweatpy!

We've put together the following guidelines to help you figure out where you can best be helpful.

## Types of contributions we are looking for
There are many ways you can directly contribute to this project:

Contributing to documentation:
* Notify us of errors in the documentation or provide fixes for them.
* Suggest or provide additions to the documentation.

Contributing to code:
* Notify us of bugs in our code or provide fixes for them.
* Suggest or provide new features.

Interested in making a contribution? Read on!

## Ground rules & expectations

Before we get started, here are a few things we expect from you (and that you should expect from others):

* Be kind and thoughtful in your conversations around this project. Try to listen to others rather than convince them that your way is correct.
* Be considerate that the maintainers of this project do their work on a voluntary basis: Do not expect commercial support when you did not pay for it.
* If you open a pull request, please ensure that your contribution passes all tests. If there are test failures, you will need to address them before we can merge your contribution.
* When adding content, please consider if it is widely valuable.

## How to contribute

If you'd like to contribute, start by searching through the [issues](https://github.com/goldencheetah/sweatpy/issues) and [pull requests](https://github.com/goldencheetah/sweatpy/pulls) to see whether someone else has raised a similar idea or question.

If you don't see your idea listed, and you think it fits into the goals of this project, do one of the following:
* **If your contribution is minor,** such as a typo fix, open a pull request.
* **If your contribution is major,** such as a new guide, start by opening an issue first. That way, other people can weigh in on the discussion before you do any work.

## Setting up your environment

For basic contributions like additions to the docs there are no requirements besides access to git and a text editor.

If you are doing code changes you need to have `docker` an `docker-compose` installed to run the test suite. Instructions can be found [here](https://docs.docker.com/compose/install/).

> Side note: The test suite can be run outside docker but requires installing `poetry` and `pyenv` locally. In most cases using the docker workflow is easiest.

To run the full (i.e. for all supported Python versions) test suite:
```bash
make testall
```
...or the equivalent command (see [Makefile](Makefile)):
```bash
docker run -it --rm --cpus="3" -v ${PWD}/.tox:/src/.tox sweatpy-test
```

For a short test run you can also run it for only 1 Python version (usually the latest major version; currently 3.8):
```bash
make test
```
...or equivalently:
```bash
docker run -it --rm -v ${PWD}/.tox:/src/.tox sweatpy-test tox -e py38
```
