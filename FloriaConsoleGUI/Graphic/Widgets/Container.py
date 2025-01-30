from typing import Union, Iterable, overload

from ..BaseGraphicObject import BaseGraphicContainerObject
from .Widget import Widget
from ..Pixel import Pixel
from ...Classes import *

class Container(BaseGraphicContainerObject, Widget):
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
        objects: Union[Iterable[Widget], Widget] = [], 
        size_by_objects: bool = True,
        objects_direction: Union[Orientation, None] = None,
        gap: int = 0,
        scroll: Iterable[int] = None,
        **kwargs,
    ): ...
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)