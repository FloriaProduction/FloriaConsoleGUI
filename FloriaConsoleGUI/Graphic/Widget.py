from random import randint as rd
from typing import Union, Iterable, TypeVar

from ..Classes import Buffer, Vec2, Vec3, Event, Counter
from ..Graphic import Pixel

from .. import Converter

_T = TypeVar('_T')

class Widget:
    _widgets: dict[str, 'Widget'] = {}
    _counter: Counter = Counter()
    
    @classmethod
    def getByName(cls, name: str) -> Union['Widget', None]:
        return cls._widgets.get(name)
    
    @classmethod
    def removeAll(cls):
        cls._widgets.clear()
    
    @classmethod
    def generateNewWidgetWithName(cls, widget_class: _T, *args, **kwargs) -> _T:
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
        self._clear_pixel: Union[Pixel, None] = Converter.toPixel(clear_pixel)
        self._size = Converter.toVec2(size)
        self._offset_pos = Converter.toVec3(offset_pos)
        self._buffer: Buffer[Pixel] = None
        
        self._flag_refresh: bool = True
        
        self._set_refreshing_event: Event = Event()
        
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
        return self._set_refreshing_event
    
    def __str__(self, **kwargs):
        kwargs.update({
            "name": self._name,
            "size": self._size,
            "offset_pos": self._offset_pos
        })
        return f'{self.__class__.__name__}({'; '.join([f'{key}:{value}' for key, value in kwargs.items()])})'