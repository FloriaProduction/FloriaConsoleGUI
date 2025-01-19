from typing import Union, Iterable

from .Widget import Widget
from ..Pixel import Pixel, Pixels
from ...Classes import Vec2, Vec3, Vec4, Buffer
from ... import Converter


class ProgressBar(Widget):
    def __init__(
        self, 
        size: Union[Vec2[int], Iterable[int]] = None,
        min_size: Union[Vec2[Union[int, None]], Iterable[Union[int, None]], None] = None,
        max_size: Union[Vec2[Union[int, None]], Iterable[Union[int, None]], None] = None,
        padding: Union[Vec4[int], Iterable[int]] = None,
        offset_pos: Union[Vec3[int], Iterable[int]] = None, 
        clear_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str, None] = None,
        name: Union[str, None] = None,
        percent: float = 0,
        progress_bar_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str, None] = Pixels.b_white,
        can_be_moved: bool = True,
        *args, **kwargs
    ):
        '''
            percent: 0-1
        '''
        super().__init__(
            size=size,
            min_size=min_size,
            max_size=max_size,
            padding=padding, 
            offset_pos=offset_pos, 
            clear_pixel=clear_pixel, 
            name=name, 
            can_be_moved=can_be_moved,
            *args, **kwargs
        )
        
        self._percent = percent
        self._progress_bar_pixel = Converter.toPixel(progress_bar_pixel)
    
    async def refresh(self):
        await super().refresh()
        
        self._buffer.paste(
            self.padding.left, 
            self.padding.top,
            Buffer(
                max(min(round(self._size.x * self._percent), self._size.x), 0), 
                self._size.y,
                self._progress_bar_pixel
            )
        )
    
    @property
    def percent(self) -> float:
        '''
            from 0 to 1
        '''
        return self._percent
    @percent.setter
    def percent(self, value: float):
        self._percent = max(min(value, 1), 0)
        self.setFlagRefresh()
        
        

