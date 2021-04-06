# Contributing

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

!!! note
    The test suite can be run outside docker but requires installing `poetry` and `pyenv` locally. In most cases using the docker workflow is easiest.

## Code contributions
The code for this library is located in the `sweat/` directory.
Tests are located in `tests/`.

### Running tests
To run the full (i.e. for all supported Python versions) test suite:
```bash
make testall
```
...or the equivalent `docker-compose` command (see [Makefile](Makefile)).

For a short test run you can also run it for only 1 Python version (usually the latest major version; currently 3.8):
```bash
make test
```
...or the equivalent `docker-compose` command.

To run tests only for a specific Python version, like Python 3.8:
```bash
toxargs="-e py38" make test
```
For a list of available Python version, see the `envlist` variable in `pyproject.toml`.
The `toxargs` environment variable can also be used to pass other settings to [tox](https://tox.readthedocs.io/en/latest/).

To only run specific tests, e.g. only that match "test_read_fit":
```bash
pytestargs="-k test_read_fit" make test
```
See the [pytest documentation](https://docs.pytest.org/en/stable/usage.html#specifying-tests-selecting-tests) for more information on selecting tests.
The `pytestargs` environment variable can also be used to pass other settings to [pytest](https://docs.pytest.org/en/stable/).

Code linting checks can be run with `make lint` or the equivalent `docker-compose` command.

### Git flow
If you're new to git, [this](https://try.github.io/) is a good place to start.

For this project we adopted a slightly modified version of the [Gitflow Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) (or more specifically, the [Forking workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/forking-workflow).
The difference is that we only work with a master branch in the central repository, so all pull requests are made from feature branches in the forked repositories directly to the master branch of the central repository.
We realize that there are downsides to this flow but as it is easiest for maintainers we decided to adopt it.

The general workflow will be:
- Create a fork of the central repository and check it out locally if you have not done so yet.
- Create a new feature branch (`feature/{your_new_feature}`)
- Make all the required changes in the repo.
- Commit your changes in a single commit and push to your fork.
- Create a pull request from the feature branch in your fork to the master branch of the central repository.
- When all checks pass, your changes will be merged to master.  

### Requirements for merging code
This list is not perfect, probably not complete and probably overly strict as well. We use it as a general guide line for all contributions to our code.

- New features should be generic and not specific to one user or use-case.
- New features should be properly unittested. Take a look at existings tests to get you started. Do not forget to test your [unhappy paths](https://en.wikipedia.org/wiki/Happy_path) too!
- All tests should pass.
- The code should pass the linting check with Black.
- New features should include some documentation with at least a basic example.
- New features that include models or algorithms should state where it is coming from (e.g. a scientific article) in the documentation.


## Documentation contributions
Documentation is built with [mkdocs](https://www.mkdocs.org/) with the [mkdocs-material](https://squidfunk.github.io/mkdocs-material/) theme and is located in the `docs/` directory.
Confusingly (but that's how mkdocs works by default so we kept it that way) the actual source files of the docs are in the `docs/docs/` directory.
The home page (or root of the docs) is `docs/docs/index.md`.

New markdown files that are added to the `docs/docs/` directory are rendered as sub-pages and automatically added to the left navigation pane.
New directories that are added to the `docs/docs/` directory are added as new sections and automatically added also added to the left navigation pane.

To run the docs dev-server run `make docs` (or the equivalent `docker-compose` command, see the `Makefile`). The documentation is now available for you at [http://localhost:8000](http://localhost:8000).
The `make docs` command also runs a Jupyter notebook server at [http://localhost:8888](http://localhost:8888) which can be used to easily create documentation with code examples (please note that you can also add inline code blocks in regular markdown files). Jupyter notebook files (ending in ".ipynb") are automatically rendered as documentation too.

- More information on working with markdown can be found [here](https://guides.github.com/features/mastering-markdown/).
- More information on working with Jupyter notebooks can be found [here](https://jupyter-notebook.readthedocs.io/en/stable/notebook.html).

## Example data
Example data is stored in `/sweat/examples/data/`.
Every new data that is added needs to be added to `sweat/examples/index.yml` too.
See [Example data](features/example_data.md) for how to use the example data.

## Continuous integration and continuous deployment
This repo is setup with Github Actions that are triggered on specific events:

* The test suite and linting checks are triggered at each push and pull request.
* When a new release is created on the central repo, a new version of this package is published to PyPi and new documentation is published.

*(This document is very much inspired by opensource.guide's [CONTRIBUTING.md](https://github.com/github/opensource.guide/blob/master/CONTRIBUTING.md))*

## FIT profile
The Profile.xlsx that is included in the Garmin FIT SDK (https://developer.garmin.com/fit/download/) is included in the source code as a JSON file (`sweat/io/fit_profile.jons`).
Garmin regularly updates this file when new devices are introduced.
Updating the JSON can be done by running:
```python
from sweat.io import fit
fit._import_fit_profile("path/to/new/Profile.xlsx")
```
...the new JSON file is than replaced in the source directory.
