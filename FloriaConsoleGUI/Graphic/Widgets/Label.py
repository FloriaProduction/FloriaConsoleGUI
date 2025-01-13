from typing import Union, Iterable

from .Widget import Widget
from ..Pixel import Pixel, Pixels
from ...Classes import Vec2, Vec3, Anchor
from ... import Func
from ... import Converter

class Label(Widget):
    def __init__(
        self, 
        text: str = 'label', 
        offset_pos: Union[Vec3[int], Iterable[int]] = None, 
        clear_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str, None] = None,
        name: Union[str, None] = None,
        min_size: Union[Vec2[Union[int, None]], Iterable[Union[int, None]], None] = None,
        anchor: Union[Anchor, str] = Anchor.left,
        tab_length: int = 4,
        *args, **kwargs
    ):
        super().__init__((0, 0), offset_pos, clear_pixel, name, *args, **kwargs)
        
        self._anchor = Converter.toAnchor(anchor)
        self._min_size = Converter.toVec2(min_size, Vec2(None, None), True)
        self._lines: tuple[str] = ()
        self._tab_length = tab_length
        
        self.text = text
    
    def refresh(self):
        super().refresh()
        for y in range(len(self._lines)):
            for x in range(len(self._lines[y])):
                self._buffer[
                    x + self.padding.z, 
                    y + self.padding.x
                ] = Pixel.changePixel(
                    self._clear_pixel if self._clear_pixel is not None else Pixels.f_white, 
                    symbol=self._lines[y][x]
                )
    
    @property
    def text(self) -> str:
        return '\n'.join(self._lines)
    @text.setter
    def text(self, value: str):
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

