from random import randint as rd
from typing import Union, Iterable, TypeVar

from .. import BaseGraphicObject, Pixel
from ...Classes import Buffer, Vec2, Vec3, Event, Counter

from ... import Converter

class Widget(BaseGraphicObject):
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
        clear_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str] = None,
        name: Union[str, None] = None,
        *args, **kwargs
        ):
        super().__init__(
            size=size, 
            offset_pos=offset_pos, 
            clear_pixel=clear_pixel, 
            name=name, 
            *args, **kwargs
        )
        
        if self.name is not None:
            if self.name in self.__class__._widgets:
                raise ValueError(f'Widget name "{self._name}" already used')
            self.__class__._widgets[self.name] = self