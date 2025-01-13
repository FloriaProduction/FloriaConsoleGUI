from typing import Union, Iterable

from ..BaseGraphicObject import BaseGraphicContainerObject
from .Widget import Widget
from ..Pixel import Pixel
from ...Classes import Vec2, Vec3
from ..Drawer import Drawer
from ... import Converter
from ... import Func

class Container(Widget, BaseGraphicContainerObject):
    def __init__(
        self, 
        size: Union[Vec2[int], Iterable[int]] = None,
        auto_size: bool = False,
        offset_pos: Union[Vec3[int], Iterable[int]] = None, 
        clear_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str] = None,
        name: Union[str, None] = None,
        widgets: Union[Iterable[Widget], Widget] = None, 
        *args, **kwargs
    ):
        super().__init__( 
            size=size,
            auto_size=auto_size,
            offset_pos=offset_pos,
            clear_pixel=clear_pixel,
            name=name,
            objects=widgets,
            *args, **kwargs
        )
