from typing import Union, Iterable

from ...Classes import Vec2, Vec3, Vec4, Event, Anchor
from .Label import Label
from .InteractiveWidget import InteractiveWidget
from ..Pixel import Pixel
from ... import Converter


class InteractiveLabel(Label, InteractiveWidget):
    def __init__(
        self, 
        text: str = 'InteractiveWidget',
        text_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str, None] = None,
        text_anchor: Anchor = Anchor.left,
        text_max_size: Union[Vec2[int], Iterable[int]] = None,
        size: Union[Vec2[int], Iterable[int]] = None,
        min_size: Union[Vec2[Union[int, None]], Iterable[Union[int, None]], None] = None,
        max_size: Union[Vec2[Union[int, None]], Iterable[Union[int, None]], None] = None,
        padding: Union[Vec4[int], Iterable[int]] = None,
        offset_pos: Union[Vec3[int], Iterable[int]] = None, 
        clear_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str] = None,
        name: Union[str, None] = None,
        tabindex: Union[int, None] = None,
        select_clear_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str] = None,
        can_be_moved: bool = True,
        *args, **kwargs
        ):
        super().__init__(
            text=text,
            text_pixel=text_pixel,
            text_anchor=text_anchor,
            text_max_size=text_max_size,
            size=size, 
            min_size=min_size,
            max_size=max_size,
            padding=padding, 
            offset_pos=offset_pos, 
            clear_pixel=clear_pixel, 
            name=name, 
            can_be_moved=can_be_moved,
            tabindex=tabindex,
            select_clear_pixel=select_clear_pixel,
            *args, **kwargs
        )


    