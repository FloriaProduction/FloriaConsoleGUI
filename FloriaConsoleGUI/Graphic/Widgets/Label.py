from typing import Union, Iterable

from .Widget import Widget
from ..Pixel import Pixel, Pixels
from ...Classes import Vec2, Vec3, Vec4, Anchor
from ... import Func
from ... import Converter

class Label(Widget):
    def __init__(
        self, 
        text: str = 'label', 
        text_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str, None] = None,
        padding: Union[Vec4[int], Iterable[int]] = None,
        offset_pos: Union[Vec3[int], Iterable[int]] = None, 
        clear_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str, None] = None,
        name: Union[str, None] = None,
        min_size: Union[Vec2[Union[int, None]], Iterable[Union[int, None]], None] = None,
        anchor: Union[Anchor, str] = Anchor.left,
        tab_length: int = 4,
        *args, **kwargs
    ):
        super().__init__(
            size=(0, 0), 
            padding=padding,
            offset_pos=offset_pos, 
            clear_pixel=clear_pixel, 
            name=name, 
            *args, **kwargs
        )
        
        self._text_pixel = Converter.toPixel(text_pixel)
        self._anchor = Converter.toAnchor(anchor)
        self._min_size = Converter.toVec2(min_size, Vec2(None, None), True)
        self._lines: tuple[str] = ()
        self._tab_length = tab_length
        
        self.text = text
    
    def refresh(self):
        super().refresh()
        
        text_pixel = Func.choisePixel(self.text_pixel, self.clear_pixel, Pixels.wt)
        for y in range(len(self._lines)):
            for x in range(len(self._lines[y])):
                self._buffer[
                    x + self.padding.left, 
                    y + self.padding.top
                ] = Pixel.changePixel(text_pixel, symbol=self._lines[y][x])
    
    def setText(self, value: str):
        text = str(value).replace('\t', ' '*self._tab_length)
        self._lines = tuple([
            Func.setTextAnchor(
                line, 
                self._anchor, 
                max(len(line), self._min_size.x),
                self._clear_pixel.symbol
            ) if self._min_size.x is not None else line for line in [
                line.replace('\n', '') for line in text.rsplit('\n')
            ]
        ])
        
        self.size = Vec2(
            max(map(len, self._lines)), 
            len(self._lines)
        )
        
        self.setFlagRefresh()
        
    def getText(self) -> str:
        return '\n'.join(self._lines)
    @property
    def text(self) -> str:
        return self.getText()
    @text.setter
    def text(self, value: str):
        self.setText(value)
    
    @property
    def text_pixel(self) -> Union[Pixel, None]:
        return self._text_pixel
    @text_pixel.setter
    def text_pixel(self, value: Union[Pixel, None]):
        self._text_pixel= value

