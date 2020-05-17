import enum
import re

from . import data


class RawRuleIndex(enum.IntEnum):
    recognizer_type = 0
    recognizer_value = enum.auto()
    color = enum.auto()
    comment = enum.auto()


class Rules:
    separator = r"\s{4}\s*"

    def parse(self, raw_rules: [str]):
        try:
            return self._parse_rules(raw_rules)
        except Exception as e:
            raise LocomRuleParserException("Parsing rules failed.")

    def _parse_rules(self, raw_rules: [str]):
        rules = []

        for raw_rule in raw_rules:
            rule = self._parse_rule(raw_rule)
            rules.append(rule)

        return rules

    def _parse_rule(self, raw_rule: str) -> data.Rule:
        parts = re.split(self.separator, raw_rule.strip())
        rule = data.Rule()

        rule.recognizer.type = parts[RawRuleIndex.recognizer_type]
        rule.recognizer.value = parts[RawRuleIndex.recognizer_value]
        rule.render.type = parts[RawRuleIndex.color]
        rule.render.comment = self._parse_comment(parts)

        return rule

    def _parse_comment(self, parts: [str]) -> str:
        if len(parts) == 4:
            return parts[RawRuleIndex.comment].strip()
        else:
            return ""


class LocomRuleParserException(Exception):
    pass