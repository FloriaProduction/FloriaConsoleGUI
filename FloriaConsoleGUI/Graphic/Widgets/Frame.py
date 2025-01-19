from typing import Union, Iterable

from .Container import Container
from .Widget import Widget
from ..Pixel import Pixel, Pixels
from ...Classes import Vec2, Vec3, Vec4, Orientation
from ..Drawer import Drawer
from ... import Func, Converter


class Frame(Container):
    def __init__(
        self, 
        size: Union[Vec2[int], Iterable[int]] = None,
        min_size: Union[Vec2[Union[int, None]], Iterable[Union[int, None]], None] = None,
        max_size: Union[Vec2[Union[int, None]], Iterable[Union[int, None]], None] = None,
        padding: Union[Vec4[int], Iterable[int]] = None,
        auto_size: bool = False,
        offset_pos: Union[Vec3[int], Iterable[int]] = None, 
        clear_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str] = None,
        frame_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str] = None, 
        name: Union[str, None] = None,
        widgets: Union[Iterable[Widget], Widget] = None,
        direction: Union[Orientation, None] = Orientation.horizontal,
        gap: int = 0,
        can_be_moved: bool = True,
        *args, **kwargs
    ):
        super().__init__(
            size=size,
            min_size=min_size,
            max_size=max_size,
            padding=padding,
            auto_size=auto_size, 
            offset_pos=offset_pos, 
            clear_pixel=clear_pixel, 
            name=name, 
            widgets=widgets, 
            direction=direction,
            gap=gap,
            can_be_moved=can_be_moved,
            *args, **kwargs
        )
        
        self._frame_pixel = Converter.toPixel(frame_pixel)
    
    def getPadding(self):
        return super().getPadding() + Vec4(1, 1, 1, 1)
        
    async def refresh(self):
        await super().refresh()
        
        frame_pixel: Pixel = Func.choisePixel(
            self.frame_pixel, 
            self.clear_pixel, 
            default=Pixels.white_black
        )
        
        self._buffer.paste(
            0, 0,
            Drawer.frame(
                self.width + self.padding.horizontal,
                self.height + self.padding.vertical, 
                frame_pixel.front_color,
                frame_pixel.back_color
            ),
            func=Drawer.mergeFramePixels
        )
    
    @property
    def frame_pixel(self) -> Pixel:
        return self._frame_pixel
    @frame_pixel.setter
    def frame_pixel(self, value: Union[Pixel, None]):
        self._frame_pixel = value
    
        

