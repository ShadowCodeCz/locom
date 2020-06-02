import enum


class LocomException(Exception):
    pass


class RawRuleIndex(enum.IntEnum):
    recognizer_type = 0
    recognizer_value = enum.auto()
    styles = enum.auto()
    text = enum.auto()
    detail = enum.auto()


class ColorIndex(enum.IntEnum):
    major_style = 0
    minor_style = enum.auto()


class RuleSetting:
    def __init__(self):
        self.recognizer = RecognizerSetting()
        self.highlight = HighlightSetting()


class RecognizerType:
    re = "re"
    row = "row"


class RecognizerSetting:
    def __init__(self):
        self.type = None
        self.value = None
        # self.orientation = None


class HighlightOrientation:
    horizontal = "horizontal"
    left = "left"
    right = "right"


class HighlightSetting:
    def __init__(self):
        self.orientation = None
        self.major_style = None
        self.minor_style = None
        self.text = None
        self.detail = None


class RenderSetting:
    def __init__(self):
        self.whitespace_protection = None
        self.escape_sequence_protection = None


class AnnotatedRow:
    def __init__(self, number, text):
        self.number = number
        self.text = text
        self.highlights = []
        self.horizontal_style = "normal"
        self.vertical_style = {VerticalColumn.left: "normal", VerticalColumn.right: "normal"}
        self.rowspan = {VerticalColumn.left: 0, VerticalColumn.right: 0}


class VerticalColumn:
    left = "left"
    right = "right"


continuing_vertical_highlight = -1


class RenderElementType:
    title = "TITLE"
    source_file = "SOURCE_FILE"
    description = "DESCRIPTION"
    multi_row_column = "MULTI_ROW_COLUMN"
    row_number_column = "ROW_NUMBER_COLUMN"
    log_column = "LOG_COLUMN"
    comment_column = "COMMENT_COLUMN"
    rows = "ROWS"


class RenderRows(list):
    type = RenderElementType.rows


class RenderElement:
    def __init__(self, type, text):
        self.type = type
        self.text = text