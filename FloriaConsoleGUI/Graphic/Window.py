from typing import Union, Iterable
import numpy as np 

from ..Classes import Buffer, Event, Vec2, Vec3
from .Pixel import Pixel
from .Widget import Widget
from .Drawer import Drawer
from .. import Converter

class Window:
    _windows: dict[str, 'Window'] = {}
    
    @classmethod
    def getWindow(cls, name: str) -> Union['Window', None]:
        return cls._windows.get(name)
    
    @classmethod
    def removeAll(cls):
        cls._windows.clear()
    
    def __init__(
            self, 
            size: Union[Vec2[int], Iterable[int]] = None, 
            offset_pos: Union[Vec3[int], Iterable[int]] = None, 
            widgets: Union[Iterable[Widget], Widget] = None, 
            clear_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str] = None,
            frame: bool = False,
            name: Union[str, None] = None,
            *args, **kwargs
        ):
        self._size = Converter.toVec2(size)
        self._offset_pos = Converter.toVec3(offset_pos)
        
        self._frame: bool = frame
        
        self._offset_widgets: Vec3[int] = Vec3(0, 0, 0)
        
        self._widgets: list[Widget] = Converter.toListWidgets(widgets)
        
        self._clear_pixel = Converter.toPixel(clear_pixel)
        
        self._open_event: Event = Event()
        self._close_event: Event = Event()
        
        self._name = name
        if self._name is not None:
            if self._name in self.__class__._windows:
                raise ValueError(f'name "{self._name}" already used')
            self.__class__._windows[self._name] = self
    
    def __del__(self):
        if self.name is not None:
            self.__class__._windows.pop(self.name)
    
    def addWidget(self, widget: Widget):
        self._widgets.append(widget)
    
    def render(self) -> Buffer[Pixel]:
        buffer = Buffer(*self._size, self._clear_pixel)

        for widget in sorted(self._widgets, key=lambda widget: widget.offset_pos.z):
            buffer.paste(
                *((widget.offset_pos + (
                    Vec3(1, 1, 0) if self._frame else Vec3(0, 0, 0)
                ) + self._offset_widgets).toTuple()[:2]), 
                widget.render(),
                Drawer.mergeFramePixels
            )
        
        if self._frame:
            buffer.paste(
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
        return buffer
            
    @property
    def offset_pos(self) -> Vec3[int]:
        return self._offset_pos
    @offset_pos.setter
    def offset_pos(self, value: Vec3[int]):
        self._offset_pos = value
    @property
    def offset_x(self) -> int:
        return self._offset_pos.x
    @property
    def offset_y(self) -> int:
        return self._offset_pos.y
    @property
    def offset_z(self) -> int:
        return self._offset_pos.z
    @property
    def width(self) -> int:
        return self._size.x
    @property
    def height(self) -> int:
        return self._size.y
    @property
    def name(self) -> Union[str, None]:
        return self._name