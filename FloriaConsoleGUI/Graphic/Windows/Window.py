from typing import Union, Iterable
import numpy as np 

from ..__init__ import BaseGraphicObject, BaseGraphicContainerObject, Pixel, Pixels, Drawer
from ..Widgets import Widget
from ...Classes import Buffer, Event, Vec2, Vec3, Vec4

from ... import Converter
from ... import Func

class Window(BaseGraphicContainerObject):    
    def __init__(
        self, 
        size: Union[Vec2[int], Iterable[int]] = None,
        auto_size: bool = False,
        offset_pos: Union[Vec3[int], Iterable[int]] = None, 
        clear_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str] = None,
        name: Union[str, None] = None,
        widgets: Union[Iterable[Widget], Widget] = [], 
        frame: bool = False,
        frame_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str] = None,
        *args, **kwargs
    ):
        super().__init__(
            size=size, 
            auto_size=auto_size, 
            offset_pos=offset_pos, 
            clear_pixel=Func.choisePixel(clear_pixel, Pixel.empty), 
            name=name, 
            objects=widgets, 
        *args, **kwargs)
        
        ''' events '''
        self._open_event = Event()
        self._close_event = Event()
        self._change_frame_pixel_event = Event()
        
        ''' pixels ''' 
        self._frame_pixel = Converter.toPixel(frame_pixel)
        
        ''' other '''
        self._frame = frame
    
    def refresh(self):
        super().refresh()
        
        if self.frame:
            frame_color: Pixel = Func.choisePixel(self.frame_pixel, self.clear_pixel)
            
            self._buffer.paste(
                0, 0,
                Drawer.frame(
                    *self.size,
                    frame_color.front_color, 
                    frame_color.back_color
                )
            )
        
    def getPadding(self):
        return super().getPadding() + (
            Vec4(1, 1, 1, 1) if self.frame else Vec4(0, 0, 0, 0)
        )
    
    @property
    def open_event(self) -> Event:
        return self._open_event
    @property
    def close_event(self) -> Event:
        return self._close_event
    
    def setFrame(self, value: bool):
        self._frame = value
        self.setFlagRefresh()
    @property
    def frame(self) -> bool:
        return self._frame
    @frame.setter
    def frame(self, value: bool):
        self.setFrame(value)
    
    @property
    def frame_pixel(self) -> Union[Pixel, None]:
        return self._frame_pixel
    @frame_pixel.setter
    def frame_pixel(self, value):
        self._frame_pixel = value
        self.setFlagRefresh()
        self.change_frame_pixel_event.invoke()

    @property
    def change_frame_pixel_event(self) -> Event:
        return self._change_frame_pixel_event
