import os
import glob

from . import base
from . import parser
from . import template
from . import annotator
from . import render


def run(arguments):
    app = App(arguments)
    app.run()


# def relevant_files(suffixes, path="."):
#     base_directory = os.path.abspath(path)
#
#     files = []
#
#     for suffix in suffixes:
#         files += glob.glob(os.path.join(base_directory, suffix))
#
#     return files
#
#
# def rule_file(path):
#     basename = os.path.basename(path)
#     return os.path.join(locom_directory(path), basename)
#
#
# def locom_directory(path="."):
#     dirname = os.path.dirname(path)
#     return os.path.join(dirname, "locom")
#
#
def auto(arguments):
    pass
    # input_files = [InputFile(input_file_path) for input_file_path in CurrentDirectory.input_files(arguments.suffixes)]
#
#
# class CurrentDirectory:
#     @staticmethod
#     def input_files(suffixes):
#         return []
#
#
# class LocomRuleDirectory:
#     @property
#     def path(self):
#         pass
#
#     @staticmethod
#     def create():
#         pass


class InputFile:
    def __init__(self, path):
        self.path = path

    @property
    def rule_file(self):
        return ""


def create_empty_file(path):
    with open(path, 'a'):
        os.utime(path, None)


def generator(arguments):
    pass
    # LocomRuleDirectory.create()
    # input_files = [InputFile(input_file_path) for input_file_path in CurrentDirectory.input_files(arguments.suffixes)]
    #
    # for input_file in input_files:
    #     create_empty_file(input_file.path)


class App:
    def __init__(self, settings):
        self.settings = settings

        self.raw_rules = None
        self.rules = None
        self.rows = None
        self.template = None
        self.output = None

    def run(self):
        self._read_rules_file()
        self._parser_rules()
        self._read_input_file()
        self._read_template_file()
        self._annotate_rows()
        self._render()
        self._write_to_output_file()

    def _read_rules_file(self):
        try:
            with open(self.settings.rules_file) as rf:
                self.raw_rules = rf.readlines()
        except Exception as e:
            raise base.LocomException(f"Reading rules file '{self.settings.rules_file}' failed. {e}")

    def _parser_rules(self):
        rule_parser = parser.RulesParser()
        self.rules = rule_parser.parse(self.raw_rules)

    def _read_input_file(self):
        try:
            with open(self.settings.input_file) as i:
                self.rows = [base.AnnotatedRow(number, text) for number, text in enumerate(i.readlines(), 1)]
        except Exception as e:
            raise base.LocomException(f"Reading input file '{self.settings.input_file}' failed. {e}")

    def _read_template_file(self):
        template_loader = template.Loader()
        self.template = template_loader.load(self.settings.template)

    def _annotate_rows(self):
        row_annotator = annotator.RowAnnotator()
        row_annotator.annotate(self.rules, self.rows)

    def _render(self):
        render_setting = base.RenderSetting()

        render_setting.whitespace_protection = not self.settings.cancel_whitespace_protection
        render_setting.escape_sequence_protection = not self.settings.cancel_escape_sequence_protection

        html_render = render.HtmlRender()
        self.output = html_render.render(render_setting, self._render_elements(), self.template)

    def _render_elements(self):
        return [
            base.RenderElement(base.RenderElementType.title, self.settings.title),
            base.RenderElement(base.RenderElementType.source_file, os.path.abspath(self.settings.input_file)),
            base.RenderElement(base.RenderElementType.description, self._description()),
            base.RenderElement(base.RenderElementType.row_number_column, self.settings.row_number_column),
            base.RenderElement(base.RenderElementType.log_column, self.settings.log_column),
            base.RenderElement(base.RenderElementType.comment_column, self._count_comment_column()),
            base.RenderElement(base.RenderElementType.multi_row_column, self.settings.mr_column),
            base.RenderRows(self.rows),
        ]

    def _count_comment_column(self):
        # TODO: May be it should be outside of this class
        return str(100 - (int(self.settings.row_number_column) +
                          int(self.settings.log_column) +
                          2 * int(self.settings.mr_column))
                   )

    def _write_to_output_file(self):
        with open(self._output_file(), "w") as o:
            o.write(self.output)

    def _output_file(self):
        if self.settings.output_file == "":
            right_dot_index = self.settings.input_file.rfind(".")
            file_without_suffix = self.settings.input_file[:right_dot_index]
            file = f"{file_without_suffix}.html"
            return file
        else:
            return self.settings.output_file

    def _description(self):
        return self.settings.description + self._read_description_from_file()

    def _read_description_from_file(self):
        if not os.path.isfile(self.settings.description_file):
            return ""
        try:
            with open(self.settings.description_file) as f:
                return f.read()
        except Exception as e:
            # TODO: print warning
            return ""


