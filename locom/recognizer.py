import re
import generic_design_patterns as gdp


class AbstractRecognizer(gdp.chain.ChainNodePlugin):
    recognizer_type = ""

    def check(self, setting, row):
        return True if setting.type == self.recognizer_type else False

    def description(self):
        return self.recognizer_type


class ReRecognizer(AbstractRecognizer):
    recognizer_type = "re"

    def handle(self,  setting, row):
        return re.search(setting.value, row.text)


class RowNumberRecognizer(AbstractRecognizer):
    recognizer_type = "row"

    def handle(self,  setting, row):
        return True if int(setting.value) == int(row.number) else False


class RuleRecognizer:
    def __init__(self):
        recognizer_collectors = [gdp.plugin.SubclassPluginCollector(AbstractRecognizer)]
        self.recognizers_chain = gdp.chain.build(recognizer_collectors)

    def recognize(self, setting, row):
        return self.recognizers_chain.handle(setting, row)

