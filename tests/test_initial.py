import pytest
import argparse
import locom
import os

# TODO: Consider using of tmpdir fixture. Carefull with Travis and --basetemp.


@pytest.fixture()
def cli_arguments():
    output_file = "output.html"

    if os.path.exists(output_file):
        os.remove(output_file)

    arguments = {
        "input_file": "input.txt",
        "rules_file": "rules.txt",
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


