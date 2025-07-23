import xml.dom

from reportlab.graphics.barcode.code128 import Code128Auto

DIM = "{0:.3f}pt"


class SvgCode128(Code128Auto):
    def __init__(self, value, **kwargs):
        super().__init__(value, **kwargs)
        self._blocks: list[tuple[float, float, float, float]] = []

        # Assigned in reportlab.graphics.barcode.common.MultiWidthBarcode.computeSize
        self._width: float
        self._height: float

    def draw(self) -> None:
        raise NotImplementedError

    # Separate function for different signature.
    def draw_svg(self) -> bytes:
        # Super implementation calls self.rect(..) repeatedly.
        super().draw()

        impl = xml.dom.getDOMImplementation()
        doc = impl.createDocument("http://www.w3.org/2000/svg", "svg", None)
        root = doc.documentElement

        root.setAttribute("version", "1.1")
        root.setAttribute("width", DIM.format(self._width))
        root.setAttribute("height", DIM.format(self._height))

        drawing = doc.createElement("g")
        root.appendChild(drawing)

        bg = doc.createElement("rect")
        bg.setAttribute("width", DIM.format(self._width))
        bg.setAttribute("height", DIM.format(self._height))
        bg.setAttribute("style", "fill:#ffffff;")
        drawing.appendChild(bg)

        for block in self._blocks:
            element = doc.createElement("rect")
            element.setAttribute("x", DIM.format(block[0]))
            element.setAttribute("y", DIM.format(block[1]))
            element.setAttribute("width", DIM.format(block[2]))
            element.setAttribute("height", DIM.format(block[3]))
            element.setAttribute("style", "fill:#000000;")
            drawing.appendChild(element)

        return doc.toxml(encoding="utf-8")

    def rect(self, x: float, y: float, w: float, h: float) -> None:
        self._blocks.append((x, y, w, h))
