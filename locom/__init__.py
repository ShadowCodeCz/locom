import argparse
import os

from . import data
from . import parser
from . import recognizer
from . import render

# TODO: Add information about templates to README
# TODO: Add description to the README: how use it in the code not cli


# TODO: RecognizedRow is strange. Same for render. Consider rename
# TODO: Consider using .json config instead of cli arguments
# TODO: Summary
# TODO: GUI APP
# TODO: Review CSS and simplify
# TODO: Multi lines rules


class TemplateLoader:
    @staticmethod
    def template_directory():
        package_directory = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(package_directory, "template")

    def load(self, template_name: str) -> str:
        template_file = self.template_path(template_name)
        try:
            with open(template_file) as t:
                return t.read()
        except Exception as e:
            raise LocomException("Reading template file '%s' failed." % template_file)

    def template_path(self, template_name: str):
        filename = "%s.html" % template_name
        return os.path.join(self.template_directory(), filename)


class HtmlGenerator:
    def __init__(self):
        self.data = None
        self.render = None
        self.recognizer = recognizer.RuleRecognizer()

    def generate(self, data):
        self.data = data

        self.render = render.Html()
        self._recognize_rows()
        output = self._generate()

        return output

    def _recognize_rows(self):
        for row in self.data.input_rows:
            rr = self._recognize_row(row)
            self.data.render.rows.append(rr)

    def _recognize_row(self, row):
        rr = data.RecognizedRow()

        rr.row = row
        rr.render = data.RowRender()

        for rule in self.data.rules:
            if self.recognizer.recognize(rule.recognizer, row):
                rr.render = rule.render

        return rr

    def _generate(self):
        return self.render.render(self.data.render)


class LocomCLI:
    def __init__(self):
        self.setting = None
        self.raw_rules = None
        self.output = None
        self.data = data.HtmlGenerator()

    def run(self, setting: argparse.Namespace):
        self.setting = setting

        self.data.render.title = setting.title
        self.data.render.description = setting.description

        self._read_rules_file()
        self._parser_rules()
        self._read_input_file()
        self._read_template_file()
        self._generate_output()
        self._write_to_output_file()

    def _read_rules_file(self):
        try:
            with open(self.setting.rules_file) as rf:
                self.raw_rules = rf.readlines()
        except Exception as e:
            raise LocomException("Reading rules file '%s' failed." % self.setting.rules_file)

    def _parser_rules(self):
        rule_parser = parser.Rules()
        self.data.rules = rule_parser.parse(self.raw_rules)

    def _read_input_file(self):
        try:
            with open(self.setting.input_file) as i:
                self.data.input_rows = [data.Row(number, text) for number, text in enumerate(i.readlines(), 1)]
        except Exception as e:
            raise LocomException("Reading input file '%s' failed." % self.setting.input_file)

    def _read_template_file(self):
        template_loader = TemplateLoader()
        self.data.render.template = template_loader.load(self.setting.template)

    def _generate_output(self):
        generator = HtmlGenerator()
        self.output = generator.generate(self.data)

    def _write_to_output_file(self):
        with open(self._output_file(), "w") as o:
            o.write(self.output)

    def _output_file(self):
        if self.setting.output_file == "":
            right_dot_index = self.setting.input_file.rfind(".")
            file_without_suffix = self.setting.input_file[:right_dot_index]
            file = "%s.html" % file_without_suffix
            return file
        else:
            return self.setting.output_file


def cli(arguments):
    locom = LocomCLI()
    locom.run(arguments)


def main():
    parser = argparse.ArgumentParser(description="Locom is tool for generation commented log. "
                                                 "The output format is HTML. "
                                                 "For more information visit https://pypi.org/project/locom/.",
                                     formatter_class=argparse.RawTextHelpFormatter)
    subparsers = parser.add_subparsers()

    cli_parser = subparsers.add_parser('cli')
    cli_parser.set_defaults(func=cli)

    cli_parser.add_argument("-r", "--rules-file",
                            required=True,
                            help="Rules describes recognition and rendering of rows.")
    cli_parser.add_argument("-i", "--input-file",
                            required=True,
                            help="Input log")
    cli_parser.add_argument("-o", "--output-file",
                            default="",
                            help="If output file is empty filename will be same as input file. "
                                 "Only suffix will be .html.")
    cli_parser.add_argument("-t", "--template",
                            default="dark",
                            help="The template for output html.")
    cli_parser.add_argument("--title",
                            default="",
                            help="The title for html output page.")
    cli_parser.add_argument("--description",
                            default="",
                            help="The description for html output page.")

    arguments = parser.parse_args()
    arguments.func(arguments)


class LocomException(Exception):
    pass


if __name__ == "__main__":
    main()



