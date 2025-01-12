from typing import Union, Iterable
import numpy as np 

from ..Classes import Buffer, Event, Vec2, Vec3
from .Pixel import Pixel
from .Widget import Widget
from .Drawer import Drawer
from .. import Converter
from .. import Func

class Window:    
    def __init__(
            self, 
            size: Union[Vec2[int], Iterable[int]] = None,
            offset_pos: Union[Vec3[int], Iterable[int]] = None, 
            widgets: Union[Iterable[Widget], Widget] = None, 
            clear_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str] = None,
            frame: bool = False,
            name: Union[str, None] = None,
            auto_size: bool = False,
            *args, **kwargs
        ):
        ''' size and pos '''
        self._size = Converter.toVec2(size)
        self._auto_size = auto_size
        self._indent_size = Vec2(2, 2) if frame else Vec2(0, 0)
        self._offset_pos = Converter.toVec3(offset_pos)
        
        ''' widgets '''
        self._offset_pos_widgets: Vec3[int] = Vec3(0, 0, 0)
        self._widgets: list[Widget] = []
        for widget in Converter.toListWidgets(widgets):
            self.addWidget(widget)
        # if self._auto_size:
        #     for widget in self._widgets:
        #         widget.resize_event.add(self.setUpdateAutoSize)
        
        ''' pixels '''
        self._clear_pixel = Converter.toPixel(clear_pixel, Pixel())
        
        ''' events '''
        self._open_event: Event = Event()
        self._close_event: Event = Event()
        self._resize_event: Event = Event()
        
        ''' flags '''
        self._flag_updateAutoSize = self._auto_size
        
        ''' other '''
        self._frame: bool = frame
        self._name = name
        
    
    def addWidget(self, widget: Widget):
        self._widgets.append(widget)
        if self._auto_size:
            widget.resize_event.add(self.setUpdateAutoSize)
    
    def render(self) -> Buffer[Pixel]:
        widgets: list[tuple[any]] = []
        for widget in sorted(self._widgets, key=lambda widget: widget.offset_pos.z):
            widgets.append((
                ((widget.offset_pos + (
                    Vec3(1, 1, 0) if self._frame else Vec3(0, 0, 0)
                ) + self._offset_pos_widgets).toTuple()[:2]),
                widget.render()
            ))
        
        if self._flag_updateAutoSize:
            self._updateAutoSize()
        
        if self.size == (0, 0):
            return Buffer.empty
        
        buffer = Buffer(*self.size, self._clear_pixel)
        
        for widget in widgets:
            buffer.paste(*widget[0], widget[1])
        
        if self._frame:
            buffer.paste(
                0, 0, 
                Drawer.frame(
                    *self.size, 
                    self._clear_pixel.front_color,
                    self._clear_pixel.back_color
                ) if self._clear_pixel is not None else
                Drawer.frame(
                    *self.size, 
                    None, None
                ),
                Drawer.mergeFramePixels
            )     
                   
        return buffer
    
    def setUpdateAutoSize(self):
        self._flag_updateAutoSize = True
    
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
    def size(self) -> Vec2[int]:
        return self._size
    @size.setter
    def size(self, value: Vec2[int]):
        self._size = value
        self._size.change_event.add(lambda: self._resize_event.invoke())
        self._resize_event.invoke()
    @property
    def width(self) -> int:
        return self.size.x
    @width.setter
    def width(self, value: int):
        self.size.x = value
    @property
    def height(self) -> int:
        return self.size.y
    @height.setter
    def height(self, value: int):
        self.size.y = value
    @property
    def name(self) -> Union[str, None]:
        return self._name
    @property
    def open_event(self) -> Event:
        return self._open_event
    @property
    def close_event(self) -> Event:
        return self._close_event
    @property
    def resize_event(self) -> Event:
        return self._resize_event
    
    def _updateAutoSize(self):
        if len(self._widgets) == 0 or self._auto_size is False:
            if self._auto_size:
                self.size = Vec2(0, 0)
            return
        
        self.size = Func.calculateSizeByItems(self._widgets) + self._indent_size + self._offset_pos_widgets.toTuple()[:2]
        
        self._flag_updateAutoSize = False
    
    
    def __str__(self, **kwargs):
        kwargs.update({
            "name": self._name,
            "size": self._size,
            "offset_pos": self._offset_pos
        })
        return f'{self.__class__.__name__}({'; '.join([f'{key}:{value}' for key, value in kwargs.items()])})'