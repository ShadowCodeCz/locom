import io
import os
import base64
from PIL import Image
import generic_design_patterns as gdp


def file_suffix(path):
    return path.split(".")[-1].lower()


class AbstractDetailRender(gdp.chain.ChainNodePlugin):
    suffixes = []

    def description(self):
        return self.__class__.__name__

    def check(self, detail):
        return os.path.exists(detail) and (file_suffix(detail) in self.suffixes)


class TextDetailRender(AbstractDetailRender):
    def check(self, detail):
        # TODO: Exists bad it is not supported format
        return not os.path.exists(detail)

    def handle(self, detail):
        return f"<div>{detail}</div>"


class ImageDetailRender(AbstractDetailRender):
    suffixes = ["jpeg", "jpg", "png", "bmp"]

    def handle(self, detail):
        img = Image.open(detail)

        img_format = file_suffix(detail)
        img_format = "jpeg" if img_format == "jpg" else img_format

        buffer = io.BytesIO()
        img.save(buffer, format=img_format)
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode('ascii')

        return f'<img src="data:image/{img_format};base64,{img_base64}">'


class HtmlDetailRender(AbstractDetailRender):
    suffixes = ["html"]

    def handle(self, detail):
        with open(detail) as detail_file:
            return detail_file.read()


class DetailRender:
    def __init__(self):
        render_collectors = [gdp.plugin.SubclassPluginCollector(AbstractDetailRender)]
        self.renders_chain = gdp.chain.build(render_collectors)

    def render(self, detail):
        return self.renders_chain.handle(detail)