import generic_design_patterns as gdp


class AbstractElementRender(gdp.chain.ChainNodePlugin):
    def description(self):
        return self.__class__.__name__

    def _target_place(self, element):
        return f"==={element.type}==="
