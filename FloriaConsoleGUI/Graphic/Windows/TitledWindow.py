from typing import Union, Iterable

from ..Window import Window
from ..Widget import Widget
from ..Pixel import Pixel
from ...Classes import Vec3, Vec2, Buffer, Anchor
from ... import Func
from ... import Converter


class TitledWindow(Window):
    def __init__(
            self,
            size: Union[Vec2[int], Iterable[int]] = None, 
            offset_pos: Union[Vec3[int], Iterable[int]] = None, 
            widgets: Union[Iterable[Widget], Widget] = None, 
            clear_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str] = None,
            frame: bool = False,
            name: Union[str, None] = None,
            title: str = 'unnamed',
            title_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str] = None,
            title_anchor: Union[Anchor, str] = Anchor.center, 
            *args, **kwargs
        ):
        super().__init__(size, offset_pos, widgets, clear_pixel, frame, name, *args, **kwargs)
        
        self._title = title
        self._title_pixel = Converter.toPixel(title_pixel, Pixel((0, 0, 0), (255, 255, 255)))
        self._title_anchor = Converter.toAnchor(title_anchor)
        self._title_buffer: Buffer[Pixel] = None
        
        self.renderTitle()

    def renderTitle(self):
        self._title_buffer = Buffer(
            self.width, 1, 
            self._title_pixel, 
            (
                Pixel.changePixel(self._title_pixel, part) for part in Func.setTextAnchor(self._title, self._title_anchor, self.width)[:self.width]
            )
        )

    def render(self):
        buffer = super().render()
        
        buffer.paste(0, 0, self._title_buffer)
        
        return buffer
    
    @property
    def title(self) -> str:
        return self._title
    @title.setter
    def title(self, value: str):
        self._title = value
        self.renderTitle()
