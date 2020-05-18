import argparse

from . import data


class Html:
    def __init__(self):
        self.data = None

    def render(self, data: data.Render) -> str:
        self.data = data
        html = data.template

        html = html.replace("%%%TITLE%%%", TitleRender.render(data.title))
        html = html.replace("%%%DESCRIPTION%%%", DescriptionRender.render(data.description))
        html = html.replace("%%%LOG%%%", LogRender.render(data.rows))

        return html


class TitleRender:
    template = "<h1>%s</h1>"

    @classmethod
    def render(cls, title: str) -> str:
        return cls.template % fix_escape_sequence(title)


class DescriptionRender:
    template = """<div class="description">%s</div>"""

    @classmethod
    def render(cls, description: str) -> str:
        return cls.template % fix_escape_sequence(description)


class LogRender:
    template = """
    <table id="logTable">
        <tr class="header">
            <th style="width:5%%;"></th>
            <th style="width:61%%;"></th>
            <th style="width:34%%;"></th>
        </tr>
        %s
    </table>
    """

    @classmethod
    def render(cls, recognized_rows: [data.RecognizedRow]) -> str:
        html_rows = ""

        for recognized_row in recognized_rows:
            html_rows += RowRender.render(recognized_row)

        return cls.template % html_rows


class RowRender:
    template = """
    <tr class="%s">
        <td class="rowNumber">%s</td>
        <td class="log">%s</td>
        <td class="comment">%s</td>
    </tr>
    """

    @classmethod
    def render(cls, recognized_row: data.RecognizedRow) -> str:
        return "" if recognized_row.render.type == "hide" else cls._render_unhidden_row(recognized_row)

    @classmethod
    def _render_unhidden_row(cls, recognized_row: data.RecognizedRow) -> str:
        return cls.template % (recognized_row.render.type,
                               recognized_row.row.number,
                               fix_escape_sequence(recognized_row.row.text),
                               recognized_row.render.comment)


def fix_escape_sequence(s: str) -> str:
    fixed = s.replace("&", "&amp;")
    fixed = fixed.replace(" ", "&nbsp;")
    fixed = fixed.replace("<", "&lt;")
    fixed = fixed.replace(">", "&gt;")
    return fixed