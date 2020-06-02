import datetime
import random

from . import abstract
from . import detail_render

from .. import base


class RowsRender(abstract.AbstractElementRender):
    row_template = """
    <tr class="{}">
        {}
        <td><div class="row-number">{}</div></td>
        <td><div class="log">{}</div></td>
        <td>{}</td>
        {}
    </tr>
    """

    def check(self, setting, template, element) -> bool:
        return True if element.type == base.RenderElementType.rows else False

    def handle(self, setting,  template, element) -> str:
        self.rows = element
        self.setting = setting
        output = ""

        for row in self.rows:
            render_content = [sub_row_render.render(setting, row) for sub_row_render in self._sub_renders()]
            output += self.row_template.format(*render_content)

        return template.replace(self._target_place(element), output)

    def _sub_renders(self):
        return [RowStyleRender(),
                LeftVerticalHighlightRender(),
                RowNumberRender(),
                RowLogRender(),
                HorizontalHighlightRender(),
                RightVerticalHighlightRender()]


def fix_escape_sequence(f):
    def wrapper(*args, **kwargs) -> str:
        s = f(*args, **kwargs)
        fixed = s.replace("&", "&amp;")
        fixed = fixed.replace(" ", "&nbsp;")
        fixed = fixed.replace("<", "&lt;")
        fixed = fixed.replace(">", "&gt;")
        return fixed
    return wrapper


class RowStyleRender:
    def render(self, setting, row: base.AnnotatedRow):
        return f"{row.horizontal_style}-row"
        # if len(major_styles):
        #     return "%s-row" % major_styles[-1]
        # else:
        #     return "normal-row"


class RowNumberRender:
    def render(self, setting, row):
        return row.number


class RowLogRender:
    @fix_escape_sequence
    def render(self, setting, row):
        return row.text


class HorizontalHighlightRender:
    expander_template = """<div class="box-comment-expander"></div>"""

    highlight_template = """
            <div class="unbox-comment"><div class="%s-box-comment"><a href="#modal%s">%s</a></div>
                <div id="modal%s" class="modal-box %s-modal-box">
                    <div>
                        <div class="modal-head %s-modal-head">
                            <span class="modal-title %s-modal-title">%s</span>
                            <span class="modal-close-button %s-modal-close-button"><a class="closeWindow" href="#close">X</a></span>
                        </div>
                        <div class="modal-row-view">
                            %s %s
                        </div>
                        <div class="modal-content">%s</div>
                    </div>
                </div>

            </div>
            """

    def render(self, setting, row: base.AnnotatedRow):
        output = ""

        horizontal_highlights = [highlight for highlight in row.highlights if highlight.orientation == base.HighlightOrientation.horizontal]

        for highlight in horizontal_highlights:
                output += self._render_horizontal_highlight(row, highlight)
        output += self.expander_template
        return output

    def _render_horizontal_highlight(self, row, highlight):
        output = ""
        dt = datetime.datetime.now()
        ts = "%s_%s" % (random.randrange(0, 101, 1), int(dt.timestamp() * 1000))

        detail_style = self._detail_style(row, highlight)

        output += self.highlight_template % (
            highlight.minor_style,
            ts,
            highlight.text,
            ts,
            detail_style,
            detail_style,
            detail_style,
            highlight.text,
            detail_style,
            row.number,
            row.text,
            self._detail(highlight)
        )
        return output

    def _detail_style(self, row, highlight):

        if highlight.minor_style == "normal":
            return row.horizontal_style
        else:
            return highlight.minor_style

    def _detail(self, highlight):
        if highlight.detail != "":
            r = detail_render.DetailRender()
            return r.render(highlight.detail)
        else:
            return highlight.detail


class VerticalHighlightRender:
    side = ""
    highlight_template = """
    <div class="%s-box-comment multi-row"><a href="#modal%s">%s</a></div>
        <div id="modal%s" class="modal-box %s-modal-box">
                    <div>
                        <div class="modal-head %s-modal-head">
                            <span class="modal-title %s-modal-title">%s</span>
                            <span class="modal-close-button %s-modal-close-button"><a class="closeWindow" href="#close">X</a></span>
                        </div>
                        <div class="modal-row-view">
                            %s %s
                        </div>
                        <div class="modal-content"></div>
                    </div>
            </div>
    """
    multi_row_template = """
        <td rowspan="%s" class="%s-box-comment">
            %s    
        </td>
    """

    def render(self, setting, row: base.AnnotatedRow):
        highlights = ""

        if row.rowspan[self.side] == base.continuing_vertical_highlight:
            print("A %s" % row.text)
            return ""
        if row.rowspan[self.side] == 0:
            print("B %s" % row.text)
            return "<td></td>"

        print("- - - - C %s" % row.text)

        vertical_highlights = [highlight for highlight in row.highlights if highlight.orientation == self.side]

        for highlight in vertical_highlights:
            highlights += self._render_vertical_highlight(row, highlight)

        # if highlights == "":
        #     if row.rowspan[self.side] == base.continuing_vertical_highlight:
        #         return ""
        #     elif row.rowspan[self.side] == 0:
        #         return "<td></td>"
        # else:
        #     return self.multi_row_template % (
        #         row.rowspan[self.side],
        #         row.vertical_style,
        #         highlights
        #     )

        return self.multi_row_template % (
            row.rowspan[self.side],
            fix_style(row.vertical_style[self.side]),
            highlights
        )

    def _render_vertical_highlight(self, row, highlight):
        output = ""
        dt = datetime.datetime.now()
        ts = "%s_%s" % (random.randrange(0, 101, 1), int(dt.timestamp() * 1000))

        detail_style = fix_style(row.vertical_style[self.side])

        output += self.highlight_template % (
            highlight.minor_style,
            ts,
            highlight.text,
            ts,
            detail_style,
            detail_style,
            detail_style,
            highlight.text,
            detail_style,
            "MULTI ROW: ",
            "%s - %s" % (row.number, row.number + row.rowspan[self.side])
        )
        return output


class LeftVerticalHighlightRender(VerticalHighlightRender):
    side = base.HighlightOrientation.left


class RightVerticalHighlightRender(VerticalHighlightRender):
    side = base.HighlightOrientation.right


def fix_style(style):
    return style.replace("left-", "").replace("right-", "")