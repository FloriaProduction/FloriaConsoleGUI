from typing import Union, Iterable

from ...Classes import Vec2, Vec3, Vec4, Event, Anchor
from .Label import Label
from ..Pixel import Pixel
from ... import Converter


class InteractiveWidget(Label):
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
            *args, **kwargs
        )
        self._selected_event = Event()
        self._not_selected_event = Event()
        
        self._select_clear_pixel = Converter.toPixel(select_clear_pixel)
        self._tabindex = tabindex
        self._selected: bool = False
    
    def inputKey(self, key: str) -> bool:
        '''
            return True if the key is processed else False
        '''
        return False
    
    def getClearPixel(self) -> Union[Pixel, None]:
        return self.select_clear_pixel if self.selected else super().getClearPixel()
    
    @property
    def tabindex(self) -> Union[int, None]:
        ''' wip '''
        return self._tabindex
    
    @property
    def selected(self) -> bool:
        return self._selected
    @selected.setter
    def selected(self, value: bool):
        if self._selected != value:
            if value:
                self._selected_event.invoke()
            else:
                self._not_selected_event.invoke()
        
        self._selected = value
        
        self.setFlagRefresh()
    
    @property
    def select_clear_pixel(self) -> Union[Pixel, None]:
        return self._select_clear_pixel
    @select_clear_pixel.setter
    def select_clear_pixel(self, value: Union[Pixel, None]):
        self._select_clear_pixel = value
    
    @property
    def selected_event(self) -> Event:
        return self._selected_event
    
    @property
    def not_selected_event(self) -> Event:
        return self._not_selected_event
    