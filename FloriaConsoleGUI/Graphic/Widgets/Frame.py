from typing import Union, Iterable

from .Container import Container
from ..Widget import Widget
from ..Pixel import Pixel
from ...Classes import Vec2, Vec3
from ..Drawer import Drawer

class Frame(Container):
    def __init__(
        self, 
        size: Union[Vec2[int], Iterable[int]] = None, 
        offset_pos: Union[Vec3[int], Iterable[int]] = None, 
        clear_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str, None] = None,
        name: Union[str, None] = None,
        widgets: Union[Iterable[Widget], Widget] = None, 
        *args, **kwargs
    ):
        super().__init__(size, offset_pos, clear_pixel, name, widgets, *args, **kwargs)

        self._offset_widgets = Vec3(1, 1, 0)
        
    def refresh(self):
        super().refresh()
        self._buffer.paste(
            0, 0,
            Drawer.frame(
                *self._size, 
                self._clear_pixel.front_color,
                self._clear_pixel.back_color
            ) if self._clear_pixel is not None else
            Drawer.frame(
                *self._size, 
                None, None
            ),
            Drawer.mergeFramePixels
        )
    
    
        

