from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd
import pytest

import sweat
from sweat.examples.utils import FileTypeEnum
from sweat.io import generic


def test_top_level_import():
    assert sweat.read_file == generic.read_file
    assert sweat.read_dir == generic.read_dir


@pytest.mark.parametrize("file_type", [(file_type) for file_type in FileTypeEnum])
def test_read_file(file_type):
    example_file = list(sweat.examples(file_type=file_type))[0]
    data = generic.read_file(example_file.path)

    assert isinstance(data, pd.DataFrame)
    assert isinstance(data.index, pd.DatetimeIndex)
    included_data = set(i.value for i in example_file.included_data)
    assert included_data <= set(data.columns.to_list())


def test_read_file_error_file_like():
    example_file = list(sweat.examples(file_type=FileTypeEnum.fit))[0]
    with example_file.path.open("r") as f:
        with pytest.raises(TypeError):
            generic.read_file(f)


def test_read_file_error_unsupported_suffix():
    fpath = Path(".", "README.md")
    with pytest.raises(ValueError):
        generic.read_file(fpath)


def test_read_dir():
    with TemporaryDirectory() as tempdir:
        tempdir = Path(tempdir)
        num_files = 0
        for file_type in FileTypeEnum:
            example_file = list(sweat.examples(file_type=file_type))[0]
            Path(tempdir, example_file.path.name).symlink_to(example_file.path)
            num_files += 1

        num_activities = 0
        for activity in generic.read_dir(tempdir):
            assert isinstance(activity, pd.DataFrame)
            num_activities += 1

        assert num_files == num_activities
