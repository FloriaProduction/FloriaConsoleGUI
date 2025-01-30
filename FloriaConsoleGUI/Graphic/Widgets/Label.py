from typing import Union, Iterable, overload

from .Widget import Widget
from ..Pixel import Pixel
from ...Classes import *
from ..Drawer import Drawer
from ... import Converter
from ... import Func

class Label(Widget):
    @overload
    def __init__(
        self,
        text: str = 'Label',
        text_anchor: Anchor = Anchor.left,
        text_pixel: Union[Pixel, tuple[Iterable[int], Iterable[int], str], str] = None,
        min_size: Union[Iterable[Union[int, None]], None] = None,
        max_size: Union[Iterable[Union[int, None]], None] = None,
        size_hint: Union[Iterable[Union[float, None]], None] = None,
        padding: Union[Iterable[int]] = None,
        offset_pos: Union[Iterable[int]] = None, 
        pos_hint: dict[str, Union[int, None]] = {},
        clear_pixel: Union[Pixel, tuple[Iterable[int], Iterable[int], str], str] = None,
        name: Union[str, None] = None,
        **kwargs
    ): ...
    
    def __init__(self, **kwargs):
        self._text: str = Converter.toMultilineText(kwargs.get('text', 'Label'))
        self._text_anchor: Anchor = Converter.toAnchor(kwargs.get('text_anchor', Anchor.left))
        self._text_pixel: Union[Pixel, None] = Converter.toPixel(kwargs.get('text_pixel'))
        self._text_buffer: Buffer[Pixel] = None
        
        super().__init__(**kwargs)
        
        self.refreshTextBuffer()
    
    async def refresh(self):
        await super().refresh()
        
        self._buffer.pasteByAnchor(
            0, 0,
            self._text_buffer,
            self.text_anchor,
            self.padding
        )
    
    def refreshTextBuffer(self, add_last_symbol: bool = False):
        self._text_buffer: Buffer[Pixel] = Drawer.renderTextBuffer(
            self.text + (' ' if add_last_symbol else ''),
            Func.choisePixel(self.text_pixel, self.clear_pixel)
        )
        self.size = self._text_buffer.size
    
    
    def getText(self) -> str:
        return self._text
    def setText(self, text: str):
        self._text = text
        self.refreshTextBuffer()
    @property
    def text(self) -> str:
        return self.getText()
    @text.setter
    def text(self, text: str):
        self.setText(text)
    
    def getTextAnchor(self) -> Anchor:
        return self._text_anchor
    def setTextAnchor(self, value: Anchor):
        self._text_anchor = value
        self.refreshTextBuffer()
    @property
    def text_anchor(self) -> Anchor:
        return self.getTextAnchor()
    @text_anchor.setter
    def text_anchor(self, value: Anchor):
        self.setTextAnchor(value)

    def getTextPixel(self) -> Union[Pixel, None]:
        return self._text_pixel
    def setTextPixel(self, value: Union[Pixel, None]):
        self._text_pixel = value
        self.refreshTextBuffer()
    @property
    def text_pixel(self) -> Union[Pixel, None]:
        return self.getTextPixel()
    @text_pixel.setter
    def text_pixel(self, value: Union[Pixel, None]):
        self._text_pixel = value
    