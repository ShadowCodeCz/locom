import re
import generic_design_patterns as gdp

from . import base


class AbstractAnnotator(gdp.chain.ChainNodePlugin):
    def handle(self, rule: base.RuleSetting, row: base.AnnotatedRow):
        row.highlights.append(rule.highlight)
        row.horizontal_style = rule.highlight.major_style


class HorizontalAnnotator(AbstractAnnotator):
    def check(self, rule: base.RuleSetting, row: base.AnnotatedRow):
        re_conditions = [
            rule.recognizer.type == base.RecognizerType.re,
            bool(re.search(str(rule.recognizer.value), row.text))
        ]

        row_conditions = [
            rule.recognizer.type == base.RecognizerType.row,
            rule.highlight.orientation == base.HighlightOrientation.horizontal,
            self._check_row_number(row, rule)
        ]

        conditions = [all(re_conditions), all(row_conditions)]

        return any(conditions)

    def _check_row_number(self, row, rule):
        try:
            return row.number in rule.recognizer.value
        except Exception as e:
            return False


class VerticalFirstRowAnnotator(AbstractAnnotator):
    def check(self, rule: base.RuleSetting, row: base.AnnotatedRow):
        conditions = [
            rule.recognizer.type == base.RecognizerType.row,
            rule.highlight.orientation != base.HighlightOrientation.horizontal,
            self._check_row_number(row, rule)
        ]

        return all(conditions)

    def handle(self, rule: base.RuleSetting, row: base.AnnotatedRow):
        row.highlights.append(rule.highlight)
        row.vertical_style[rule.highlight.orientation] = rule.highlight.major_style
        self._set_rowspan(rule, row)

    def _set_rowspan(self, rule, row):
        current_rs = row.rowspan[rule.highlight.orientation]
        rs = max([current_rs, rule.recognizer.value[-1] - rule.recognizer.value[0]])
        row.rowspan[rule.highlight.orientation] = rs


    def _check_row_number(self, row, rule):
        try:
            return row.number == rule.recognizer.value[0]
        except Exception as e:
            return False


class VerticalNextRowAnnotator(AbstractAnnotator):
    def check(self, rule: base.RuleSetting, row: base.AnnotatedRow):
        conditions = [
            rule.recognizer.type == base.RecognizerType.row,
            rule.highlight.orientation != base.HighlightOrientation.horizontal,
            self._check_row_number(row, rule)
        ]

        return all(conditions)

    def handle(self, rule: base.RuleSetting, row: base.AnnotatedRow):
        # row.vertical_style[rule.highlight.orientation] = rule.highlight.major_style
        self._set_rowspan(rule, row)

    def _set_rowspan(self, rule, row):
        current_rs = row.rowspan[rule.highlight.orientation]
        if current_rs > 0:
            rs = current_rs
        else:
            rs = base.continuing_vertical_highlight
        row.rowspan[rule.highlight.orientation] = rs

    def _check_row_number(self, row, rule):
        try:
            return row.number in rule.recognizer.value[1:]
        except Exception as e:
            return False


class RowAnnotator:
    def __init__(self):
        annotator_collectors = [gdp.plugin.SubclassPluginCollector(AbstractAnnotator)]
        self.annotators_chain = gdp.chain.build(annotator_collectors)

    def annotate(self, rules: [base.RuleSetting], rows: [base.AnnotatedRow]):
        for row in rows:
            for rule in rules:
                self.annotators_chain.handle(rule, row)



