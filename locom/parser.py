import enum
import re

from . import base


class RulesParser:
    separator = r"\s{4}\s*"

    def parse(self, raw_rules: [str]):
        try:
            return self._parse_rules(raw_rules)
        except Exception as e:
            raise base.LocomException(f"{e} Parsing rules failed.")

    def _parse_rules(self, raw_rules: [str]):
        rules = []

        for row_number, raw_rule in enumerate(raw_rules, 1):
            try:
                striped_raw_rule = raw_rule.strip()
                if striped_raw_rule == "" or striped_raw_rule[0] == "#":
                    continue
                else:
                    rule = self._parse_rule(raw_rule)
            except Exception as e:
                raise base.LocomException(f"{e} Parsing rule on row {row_number} failed.")
            rules.append(rule)

        return rules

    def _parse_rule(self, raw_rule: str) -> base.RuleSetting:
        parts = re.split(self.separator, raw_rule.strip())
        rule = base.RuleSetting()

        parts = [part.strip() for part in parts]
        parts.extend([""] * (5 - len(parts)))

        rule.recognizer.type = parts[base.RawRuleIndex.recognizer_type]
        rule.recognizer.value = parts[base.RawRuleIndex.recognizer_value]
        rule.highlight.text = parts[base.RawRuleIndex.text]
        rule.highlight.detail = parts[base.RawRuleIndex.detail]

        self._parse_styles(parts[base.RawRuleIndex.styles], rule)
        self._parse_orientation(rule)
        self._validate(rule)
        self._parse_rows(parts[base.RawRuleIndex.recognizer_value], rule)
        return rule

    def _parse_styles(self, combined_style, rule):
        parts = combined_style.split(":")

        parts.extend(["normal"] * (2 - len(parts)))

        rule.highlight.major_style = parts[base.ColorIndex.major_style]
        rule.highlight.minor_style = parts[base.ColorIndex.minor_style]

    def _parse_rows(self, raw_rows, rule):
        # TODO: protect by TRY
        if rule.recognizer.type != base.RecognizerType.re:
            r = []

            for part in raw_rows.split(","):
                sub_parts = part.split("-")

                if len(sub_parts) == 1:
                    r += [int(sub_parts[0])]

                if len(sub_parts) == 2:
                    # TODO: [0] > [1]
                    r += list(range(int(sub_parts[0]), int(sub_parts[1]) + 2))

             # TODO: Side effect! reconizer_value was originaly set in _parse_rule(). Confusing
            rule.recognizer.value = r
            rule.highlight.rows = r

    def _parse_orientation(self, rule):
        if base.HighlightOrientation.left in rule.highlight.major_style:
            self._set_orientation(rule, base.HighlightOrientation.left)

        elif base.HighlightOrientation.right in rule.highlight.major_style:
            self._set_orientation(rule, base.HighlightOrientation.right)

        else:
            self._set_orientation(rule, base.HighlightOrientation.horizontal)

    def _set_orientation(self, rule, orientation):
        rule.highlight.orientation = orientation
        rule.recognizer.orientation = orientation

    def _validate(self, rule):
        if rule.recognizer.type == "re" and rule.highlight.orientation != base.HighlightOrientation.horizontal:
            raise base.LocomException(f"Invalid combination of row recognizer ({rule.recognizer.type}) "
                                      f"and vertical highlight style ({rule.highlight.orientation}).")


