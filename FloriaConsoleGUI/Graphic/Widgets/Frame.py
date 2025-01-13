from typing import Union, Iterable

from .Container import Container
from .Widget import Widget
from ..Pixel import Pixel, Pixels
from ...Classes import Vec2, Vec3, Vec4
from ..Drawer import Drawer
from ... import Func, Converter

class Frame(Container):
    def __init__(
        self, 
        size: Union[Vec2[int], Iterable[int]] = None,
        auto_size: bool = False,
        offset_pos: Union[Vec3[int], Iterable[int]] = None, 
        clear_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str] = None,
        frame_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str] = None, 
        name: Union[str, None] = None,
        widgets: Union[Iterable[Widget], Widget] = None, 
        *args, **kwargs
    ):
        super().__init__(
            size, 
            auto_size, 
            offset_pos, 
            clear_pixel, 
            name, 
            widgets, 
            *args, **kwargs
        )
        
        self._frame_pixel = Converter.toPixel(frame_pixel)
    
    def getPadding(self):
        return super().getPadding() + Vec4(1, 1, 1, 1)
        
    def refresh(self):
        super().refresh()
        
        frame_pixel: Pixel = Func.choisePixel(
            self.frame_pixel, 
            self.clear_pixel, 
            default=Pixels.wt
        )
        
        self._buffer.paste(
            0, 0,
            Drawer.frame(
                *self._size + Vec2(2, 2), 
                frame_pixel.front_color,
                frame_pixel.back_color
            ),
            Drawer.mergeFramePixels
        )
    
    @property
    def frame_pixel(self) -> Pixel:
        return self._frame_pixel
    @frame_pixel.setter
    def frame_pixel(self, value: Union[Pixel, None]):
        self._frame_pixel = value
    
        

