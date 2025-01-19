from typing import Union, Iterable

from ..BaseGraphicObject import BaseGraphicObject
from ..Pixel import Pixel
from ...Classes import Vec2, Vec3, Vec4, Counter


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
    
    def __init__(
        self,
        size: Union[Vec2[int], Iterable[int]] = None,
        min_size: Union[Vec2[Union[int, None]], Iterable[Union[int, None]], None] = None,
        max_size: Union[Vec2[Union[int, None]], Iterable[Union[int, None]], None] = None,
        padding: Union[Vec4[int], Iterable[int]] = None,
        offset_pos: Union[Vec3[int], Iterable[int]] = None, 
        clear_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str] = None,
        name: Union[str, None] = None,
        can_be_moved: bool = True,
        *args, **kwargs
        ):
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
        
        if self.name is not None:
            if self.name in self.__class__._widgets:
                raise ValueError(f'Widget name "{self._name}" already used')
            self.__class__._widgets[self.name] = self