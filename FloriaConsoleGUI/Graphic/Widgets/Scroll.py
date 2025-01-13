from typing import Union, Iterable

from ...Classes import Vec2, Vec3, Buffer
from .Container import Container
from .Widget import Widget
from ..Pixel import Pixel, Pixels
from ... import Converter

class Scroll(Widget):
    def __init__(
        self, 
        size: Union[Vec2[int], Iterable[int]] = None, 
        offset_pos: Union[Vec3[int], Iterable[int]] = None, 
        clear_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str, None] = None,
        name: Union[str, None] = None,
        widgets: Union[Iterable[Widget], Widget] = None,
        scroll_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str, None] = None,
        *args, **kwargs
    ):
        super().__init__(size, offset_pos, clear_pixel, name, *args, **kwargs)

        self._widgets: list[Widget] = Converter.toListObjects(widgets)

        self._full_buffer: Union[Buffer[Pixel], None] = None
        self._updateFullBuffer()
        self.scroll = Vec2(0, 0)
        self._scroll_pixel = Converter.toPixel(scroll_pixel, Pixel((0, 0, 0), (255, 255, 255)))
        
    def _updateFullBuffer(self):
        max_width = max_height = 0
        
        for widget in self._widgets:
            max_width = max(max_width, widget.size.x + widget.offset_pos.x)
            max_height = max(max_height, widget.size.y + widget.offset_pos.y)

        self._full_buffer = Buffer(max_width, max_height, None)

        for widget in self._widgets:
            self._full_buffer.paste(
                *(widget.offset_pos.toTuple()[:2]),
                widget.render()
            )
    
    def refresh(self):
        if self._full_buffer is None:
            self._updateFullBuffer()
        
        super().refresh()
        
        self._buffer.paste(
            -self._scroll.x, 
            -self._scroll.y, 
            self._full_buffer
        )
        
        hor = self._full_buffer.width > self._buffer.width
        ver = self._full_buffer.height > self._buffer.height
        both = hor and ver
        
        if hor:
            for x in range(self._buffer.width):
                self._buffer[
                    x, 
                    self._buffer.height-1
                ] = self._scroll_pixel
                
            if self._scroll.x > 0:
                self._buffer[
                    0,
                    self._buffer.height-1
                ] = Pixel.changePixel(self._scroll_pixel, symbol='◄')
            
            if self._full_buffer.width - (self._scroll.x + self._buffer.width) > 0:
                self._buffer[
                    self._buffer.width-1 - (1 if both else 0), 
                    self._buffer.height-1
                ] = Pixel.changePixel(self._scroll_pixel, symbol='►')
        
        if ver:
            for y in range(self._buffer.height):
                self._buffer[
                    self._buffer.width-1, 
                    y
                ] = self._scroll_pixel
                
            if self._scroll.y > 0:
                self._buffer[
                    self._buffer.width-1, 
                    0
                ] = Pixel.changePixel(self._scroll_pixel, symbol='▲')
                
            if self._full_buffer.height - (self._scroll.y + self._buffer.height) > 0:
                self._buffer[
                    self._buffer.width-1, 
                    self._buffer.height-1 - (1 if both else 0)
                ] = Pixel.changePixel(self._scroll_pixel, symbol='▼')
        
        if hor and ver:
            self._buffer[self._buffer.width-1, self._buffer.height-1] = Pixel.changePixel(self._scroll_pixel, symbol='/')
                
    @property
    def scroll(self) -> Vec2[int]:
        return self._scroll
    @scroll.setter
    def scroll(self, value: Vec2[int]):
        def _valide_scroll():
            self._scroll._x = min(max(self._scroll.x, 0), max(self._full_buffer.width - self.size.x, 0))
            self._scroll._y = min(max(self._scroll.y, 0), max(self._full_buffer.height - self.size.y, 0))
            self.setFlagRefresh()
        
        self._scroll = value
        self._scroll.change_event.add(_valide_scroll)
        self.setFlagRefresh()
    
        


        
        
        
        
        