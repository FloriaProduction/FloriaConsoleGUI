from random import randint as rd
from typing import Union, Iterable, TypeVar

from ..Classes import Buffer, Vec2, Vec3, Event, Counter
from ..Graphic import Pixel

from .. import Converter

class Widget:
    _widgets: dict[str, 'Widget'] = {}
    _counter: Counter = Counter()
    
    @classmethod
    def getByName(cls, name: str) -> Union['Widget', None]:
        return cls._widgets.get(name)
    
    @classmethod
    def tryGetByName(cls, name: str) -> tuple[bool, Union['Widget', None]]:
        widget = cls.getByName(name)
        return (
            widget is not None,
            widget
        )
    
    @classmethod
    def removeAll(cls):
        cls._widgets.clear()
    
    @classmethod
    def generateNewWidgetWithName(cls, widget_class: 'Widget', *args, **kwargs) -> 'Widget':
        if not issubclass(widget_class, cls):
            raise ValueError(f'Class "{widget_class.__name__}" is not subclass {cls.__name__}')
        
        class_name = widget_class.__name__
        cls._counter.add(class_name)
        
        kwargs.update({
            "name": f'{class_name}_{cls._counter.get(class_name)}'
        })
        
        return widget_class(*args, **kwargs)
    
    def __init__(
        self, 
        size: Union[Vec2[int], Iterable[int]] = None, 
        offset_pos: Union[Vec3[int], Iterable[int]] = None, 
        clear_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str, None] = None,
        name: Union[str, None] = None,
        *args, **kwargs
    ):
        ''' events '''
        self._set_refreshing_event: Event = Event()
        self._resize_event: Event = Event()
        
        ''' size and pos '''
        self.size = Converter.toVec2(size)
        self._offset_pos = Converter.toVec3(offset_pos)
        
        ''' pixels '''
        self._clear_pixel: Union[Pixel, None] = Converter.toPixel(clear_pixel)
        
        ''' buffers '''
        self._buffer: Buffer[Pixel] = None
        
        ''' flags '''
        self._flag_refresh: bool = True
        
        ''' others '''
        self._name = name
        if self._name is not None:
            if self._name in self.__class__._widgets:
                raise ValueError(f'Widget name "{self._name}" already used')
            self.__class__._widgets[self._name] = self
    
    def setRefresh(self):
        self._flag_refresh = True
        self._set_refreshing_event.invoke()
    
    def refresh(self):
        self._buffer = Buffer(*self._size, self._clear_pixel)
        self._flag_refresh = False
    
    def render(self) -> Buffer[Pixel]:
        if self._flag_refresh:
            self.refresh()
            
        return self._buffer if self._buffer is not None else Buffer.empty

    @property
    def offset_pos(self) -> Vec3[int]:
        return self._offset_pos
    @property
    def offset_x(self) -> int:
        return self.offset_pos.x
    @property
    def offset_y(self) -> int:
        return self.offset_pos.y
    @property
    def offset_z(self) -> int:
        return self.offset_pos.z
    
    @property
    def size(self) -> Vec2:
        return self._size
    @size.setter
    def size(self, value: Vec2):
        self._size = Converter.toVec2(value)
        self._size.change_event.add(self.setRefresh)
        self._resize_event.invoke()
        self.setRefresh()
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
    def set_refresh_event(self) -> Event:
        return self._set_refreshing_event
    @property
    def resize_event(self) -> Event:
        return self._resize_event
    
    def __str__(self, **kwargs):
        kwargs.update({
            "name": self._name,
            "size": self._size,
            "offset_pos": self._offset_pos
        })
        return f'{self.__class__.__name__}({'; '.join([f'{key}:{value}' for key, value in kwargs.items()])})'