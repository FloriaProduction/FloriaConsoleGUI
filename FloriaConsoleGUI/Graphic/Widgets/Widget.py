from typing import Union, Iterable, overload

from ..BaseGraphicObject import BaseGraphicObject
from ..Pixel import Pixel
from ...Classes import Counter


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
    
    @overload
    def __init__(
        self,
        size: Iterable[int] = None,
        min_size: Union[Iterable[Union[int, None]], None] = None,
        max_size: Union[Iterable[Union[int, None]], None] = None,
        size_hint: Union[Iterable[Union[float, None]], None] = None,
        padding: Union[Iterable[int]] = None,
        offset_pos: Union[Iterable[int]] = None, 
        pos_hint: Union[Iterable[Union[int, None]], None] = None,
        clear_pixel: Union[Pixel, tuple[Iterable[int], Iterable[int], str], str] = None,
        name: Union[str, None] = None,
        **kwargs
    ): ...
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        if self.name is not None:
            if self.name in self.__class__._widgets:
                raise ValueError(f'Widget name "{self._name}" already used')
            self.__class__._widgets[self.name] = self