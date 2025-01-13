from typing import Union, Iterable, Unpack

from ...Classes import Vec2, Vec3, Event, Buffer
from .Widget import Widget
from ..Pixel import Pixel
from ... import Converter

class InteractiveWidget(Widget):
    def __init__(
        self, 
        size: Union[Vec2[int], Iterable[int]] = None, 
        offset_pos: Union[Vec3[int], Iterable[int]] = None, 
        clear_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str, None] = None,
        name: Union[str, None] = None,
        tabindex: Union[int, None] = None,
        select_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str, None] = None,
        *args, **kwargs):
        super().__init__(size, offset_pos, clear_pixel, name, *args, **kwargs)
        
        self._change_tabindex_event: Event = Event()
        self._tabindex: Union[int, None] = None
        self.tabindex = tabindex
        
        self._select_pixel = Converter.toPixel(select_pixel)
        self._selected: bool = False
    
    def refresh(self):
        if self._selected:
            self._buffer = Buffer(*self._size, self._select_pixel)
            print(f'interactive widtget refreshed {self}')
        else:
            super().refresh()
    
    @property
    def tabindex(self) -> Union[int, None]:
        return self._tabindex
    @tabindex.setter
    def tabindex(self, value: Union[int, None]):
        if value is not None and value < 0:
            raise ValueError('Index cannot be less than 0')
        self._tabindex = value
        self._change_tabindex_event.invoke()
    
    @property
    def change_tab_index_event(self) -> Event:
        return self._change_tabindex_event

    @property
    def selected(self) -> bool:
        return self._selected
    @selected.setter
    def selected(self, value: bool):
        if self._selected is not value:
            self._selected = value
            self.setFlagRefresh()        
    
    def __str__(self, **kwargs):
        kwargs.update({
            "tabindex": self._tabindex,
        })
        return super().__str__(**kwargs)
        
        