import pytest
from pathlib import Path
from types import GeneratorType

import sweat
from sweat.examples import utils


def test_top_level_import():
    assert sweat.examples == utils.examples
    assert sweat.FileTypeEnum == utils.FileTypeEnum
    assert sweat.SportEnum == utils.SportEnum


def test_examples():
    examples = utils.examples()

    assert isinstance(examples, list)

    first = examples[0]
    assert isinstance(first, utils.ExampleData)


def test_examples_by_path():
    path = "4078723797.fit"

    examples = utils.examples(path=path)

    assert isinstance(examples, utils.ExampleData)
    assert examples.path.name == path


def test_examples_by_path_non_existing():
    with pytest.raises(ValueError):
        utils.examples(path="some_non_existent_path.garbage")


def test_examples_by_file_type():
    file_type = utils.FileTypeEnum.fit

    examples = utils.examples(file_type=file_type)

    assert isinstance(examples, filter)

    first = next(examples)
    assert first.file_type == file_type


def test_examples_by_sport():
    sport = utils.SportEnum.cycling

    examples = utils.examples(sport=sport)
    print(type(examples))

    assert isinstance(examples, filter)

    first = next(examples)
    assert first.sport == sport


@pytest.mark.parametrize(
    "path,file_type,sport,error",
    [
        ("4078723797.fit", None, None, False),
        (None, utils.FileTypeEnum.fit, None, False),
        (None, None, utils.SportEnum.cycling, False),
        (None, utils.FileTypeEnum.fit, utils.SportEnum.cycling, False),
        ("4078723797.fit", utils.FileTypeEnum.fit, None, True),
        ("4078723797.fit", None, utils.SportEnum.cycling, True),
        ("4078723797.fit", utils.FileTypeEnum.fit, utils.SportEnum.cycling, True),
    ],
)
def test_examples_by_path_and_sport(path, file_type, sport, error):
    try:
        utils.examples(path=path, file_type=file_type, sport=sport)
    except ValueError as e:
        assert error
    else:
        pass
