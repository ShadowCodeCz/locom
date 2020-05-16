import argparse
import enum
import re
import os

from . import recognizer
from . import render

# TODO: RecognizedRow is strange. Same for render. Consider rename
# TODO: Consider using .json config instead of cli arguments
# TODO: Summary
# TODO: GUI APP
# TODO: Type annotation
# TODO: CLI help
# TODO: Review CSS and simplify


class Rule:
    def __init__(self):
        self.recognizer = RecognizerData()
        self.render = RenderData()


class RecognizerData:
    def __init__(self):
        self.type = None
        self.value = None


class RenderData:
    def __init__(self):
        self.type = None
        self.comment = None


class Row:
    def __init__(self, number, text):
        self.number = number
        self.text = text


class RecognizedRow:
    def __init__(self):
        self.original_row = None
        self.render = None


class RawRuleIndex(enum.IntEnum):
    recognizer_type = 0
    recognizer_value = enum.auto()
    color = enum.auto()
    comment = enum.auto()


class RuleParser:
    separator = r"\s{4}\s*"

    def parse(self, raw_rules: list):
        rules = []

        for raw_rule in raw_rules:
            rule = self._parse_rule(raw_rule)
            rules.append(rule)

        return rules

    def _parse_rule(self, raw_rule: str) -> Rule:
        parts = re.split(self.separator, raw_rule.strip())

        rule = Rule()

        rule.recognizer.type = parts[RawRuleIndex.recognizer_type]
        rule.recognizer.value = parts[RawRuleIndex.recognizer_value]

        rule.render.type = parts[RawRuleIndex.color]
        if len(parts) == 4:
            rule.render.comment = parts[RawRuleIndex.comment].strip()
        else:
            rule.render.comment = ""

        return rule


class TemplateLoader:
    @staticmethod
    def template_directory():
        package_directory = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(package_directory, "template")

    def load(self, template_name):
        with open(self.template_path(template_name)) as t:
            return t.read()

    def template_path(self, template_name):
        filename = "%s.html" % template_name
        return os.path.join(self.template_directory(), filename)


class LocomCLI:
    def __init__(self):
        self.setting = None
        self.rules = None
        self.template = None
        self.input_rows = None
        self.recognizer = recognizer.RuleRecognizer()
        self.recognized_rows = []
        self.render = None
        self.rendered_html = None

        self.render_not_recognized_row = RenderData()
        self.render_not_recognized_row.type = "normal"
        self.render_not_recognized_row.comment = ""

    def run(self, setting: argparse.Namespace):
        self.setting = setting
        self.render = render.Html(self.setting)

        self._parser_rule_file()
        self._read_input_file()
        self._recognize_rows()
        self._read_template_file()
        self._render()
        self._write_to_output_file()

    def _parser_rule_file(self):
        with open(self.setting.rules_file) as rf:
            raw_rules = rf.readlines()
            rule_parser = RuleParser()
            self.rules = rule_parser.parse(raw_rules)

    def _read_template_file(self):
        template_loader = TemplateLoader()
        self.template = template_loader.load(self.setting.template)

    def _read_input_file(self):
        with open(self.setting.input_file) as i:
            self.input_rows = [Row(number, text) for number, text in enumerate(i.readlines(), 1)]

    def _recognize_rows(self):
        for row in self.input_rows:
            rr = self._recognize_row(row)
            self.recognized_rows.append(rr)

    def _recognize_row(self, row):
        rr = RecognizedRow()
        rr.original_row = row
        rr.render = self.render_not_recognized_row

        for rule in self.rules:
            if self.recognizer.recognize(rule.recognizer, row):
                rr.render = rule.render

        return rr

    def _render(self):
        self.rendered_html = self.render.render(self.recognized_rows, self.template)

    def _write_to_output_file(self):
        with open(self._output_file(), "w") as o:
            o.write(self.rendered_html)

    def _output_file(self):
        if self.setting.output_file == "":
            parts = self.setting.input_file.split(".")
            file_without_suffix = "".join(parts[:-1])
            file = "%s.html" % file_without_suffix
            return file
        else:
            return self.setting.output_file


def cli(arguments):
    locom = LocomCLI()
    locom.run(arguments)


def main():
    parser = argparse.ArgumentParser(description="", formatter_class=argparse.RawTextHelpFormatter)
    subparsers = parser.add_subparsers()

    cli_parser = subparsers.add_parser('cli')
    cli_parser.set_defaults(func=cli)
    cli_parser.add_argument("-r", "--rules-file", required=True, help="")
    cli_parser.add_argument("-i", "--input-file", required=True, help="")
    cli_parser.add_argument("-o", "--output-file", default="", help="")
    cli_parser.add_argument("-t", "--template", default="dark", help="")
    cli_parser.add_argument("--title", help="")
    cli_parser.add_argument("--description", help="")

    arguments = parser.parse_args()
    arguments.func(arguments)


if __name__ == "__main__":
    main()



