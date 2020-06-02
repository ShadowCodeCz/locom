import os

from . import base


class Loader:
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
            raise base.LocomException("Reading template file '%s' failed." % template_file)

    def template_path(self, template_name: str):
        filename = "%s.html" % template_name
        return os.path.join(self.template_directory(), filename)

