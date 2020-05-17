class Rule:
    def __init__(self):
        self.recognizer = RowRecognizer()
        self.render = RowRender()


class RowRecognizer:
    def __init__(self):
        self.type = None
        self.value = None


class RowRender:
    def __init__(self):
        self.type = "normal"
        self.comment = ""


class Row:
    def __init__(self, number, text):
        self.number = number
        self.text = text


class RecognizedRow:
    def __init__(self):
        self.row = None
        self.render = None


class HtmlGenerator:
    def __init__(self):
        self.render = Render()
        self.rules = None
        self.input_rows = None


class Render:
    def __init__(self):
        self.title = None
        self.description = None
        self.template = None
        self.rows = []