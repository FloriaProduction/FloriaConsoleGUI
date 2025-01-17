from typing import Union, Iterable

from ..BaseGraphicObject import BaseGraphicContainerObject
from .Widget import Widget
from ..Pixel import Pixel
from ...Classes import Vec2, Vec3, Vec4, Orientation
from ..Drawer import Drawer
from ... import Converter
from ... import Func

class Container(BaseGraphicContainerObject, Widget):
    def __init__(
        self, 
        size: Union[Vec2[int], Iterable[int]] = None,
        min_size: Union[Vec2[Union[int, None]], Iterable[Union[int, None]], None] = None,
        max_size: Union[Vec2[Union[int, None]], Iterable[Union[int, None]], None] = None,
        padding: Union[Vec4[int], Iterable[int]] = None,
        auto_size: bool = False,
        offset_pos: Union[Vec3[int], Iterable[int]] = None, 
        clear_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str] = None,
        name: Union[str, None] = None,
        widgets: Union[Iterable[Widget], Widget] = None,
        direction: Union[Orientation, None] = Orientation.horizontal,
        gap: int = 0,
        can_be_moved: bool = True,
        *args, **kwargs
    ):
        super().__init__( 
            size=size,
            min_size=min_size,
            max_size=max_size,
            padding=padding,
            auto_size=auto_size,
            offset_pos=offset_pos,
            clear_pixel=clear_pixel,
            name=name,
            objects=widgets,
            direction=direction,
            gap=gap,
            can_be_moved=can_be_moved,
            *args, **kwargs
        )
