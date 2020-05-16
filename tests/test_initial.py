import pytest
import argparse
import locom
import os

# TODO: Consider using of tmpdir fixture. Carefull with Travis and --basetemp.


def current_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)


@pytest.fixture()
def cli_arguments():
    output_file = current_path("output.html")

    if os.path.exists(output_file):
        os.remove(output_file)

    arguments = {
        "input_file": current_path("input.txt"),
        "rules_file": current_path("rules.txt"),
        "output_file": output_file,
        "template": "dark",
        "title": "Fake title",
        "description": "Fake description"
    }

    mocked_arguments = argparse.Namespace(**arguments)

    yield mocked_arguments

    os.remove(output_file)


def test_cli_create_output_file(cli_arguments):
    locom.cli(cli_arguments)
    assert True == os.path.exists(cli_arguments.output_file)


