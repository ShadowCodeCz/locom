import generic_design_patterns as gdp

from . import abstract
from . import replacing_render
from . import row_render

# TODO: Review and rework template. Especially CSS rules.


class HtmlRender:
    def __init__(self):
        element_render_collectors = [gdp.plugin.SubclassPluginCollector(abstract.AbstractElementRender)]
        self.renders_chain = gdp.chain.build(element_render_collectors)

    def render(self, setting, elements, template) -> str:
        output = template

        for element in elements:
            output = self.renders_chain.handle(setting, output, element)

        return output



