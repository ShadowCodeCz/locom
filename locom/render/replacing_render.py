from . import abstract
from .. import base


class ReplacingRender(abstract.AbstractElementRender):
    def check(self, setting, template, element) -> bool:
        return True if element.type != base.RenderElementType.rows else False

    def handle(self, setting, template, element):
        return template.replace(self._target_place(element), str(element.text))
