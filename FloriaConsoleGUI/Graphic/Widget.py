from random import randint as rd
from typing import Union, Iterable

from ..Classes import Buffer, Vec2, Vec3, Event
from ..Graphic import Pixel

from .. import Converter

class Widget:
    _widgets: dict[str, 'Widget'] = {}
    
    @classmethod
    def getByName(cls, name: str) -> Union['Widget', None]:
        return cls._widgets.get(name)
    
    @classmethod
    def removeAll(cls):
        cls._widgets.clear()
    
    def __init__(
        self, 
        size: Union[Vec2[int], Iterable[int]] = None, 
        offset_pos: Union[Vec3[int], Iterable[int]] = None, 
        clear_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str, None] = None,
        name: Union[str, None] = None,
        *args, **kwargs
    ):
        self._clear_pixel: Union[Pixel, None] = Converter.toPixel(clear_pixel)
        self._size = Converter.toVec2(size)
        self._offset_pos = Converter.toVec3(offset_pos)
        self._buffer: Buffer[Pixel] = None
        
        self._flag_refresh: bool = True
        
        self._refreshing_event: Event = Event()
        
        self._name = name
        if self._name is not None:
            if self._name in self.__class__._widgets:
                raise ValueError(f'name "{self._name}" already used')
            self.__class__._widgets[self._name] = self
    
    def setRefresh(self):
        self._flag_refresh = True
        self._refreshing_event.invoke()
    
    def refresh(self):
        self._buffer = Buffer(*self._size, self._clear_pixel)
    
    def render(self) -> Buffer[Pixel]:
        if self._flag_refresh:
            self.refresh()
            self._flag_refresh = False
            
        return self._buffer if self._buffer is not None else Buffer.empty

    @property
    def offset_pos(self) -> Vec3[int]:
        return self._offset_pos
    
    @property
    def size(self) -> Vec2:
        return self._size
    @size.setter
    def size(self, size: Vec2):
        self._size = (size if isinstance(size, Vec2) else Vec2(*size)) if size is not None else Vec2(0, 0)
        self.setRefresh()
    
    @property
    def set_refresh_event(self) -> Event:
        return self._refreshing_event
    
    def addOffsetPos(self, pos: Vec2):
        self._offset_pos += pos