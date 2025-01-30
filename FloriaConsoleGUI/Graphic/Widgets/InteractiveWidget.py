from typing import Union, Iterable, overload

from .Widget import Widget
from ..Pixel import Pixel
from ...Classes import *
from ... import Converter


class InteractiveWidget(Widget):
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
        selected_clear_pixel: Union[Pixel, tuple[Iterable[int], Iterable[int], str], str] = None,
        name: Union[str, None] = None,
        **kwargs
    ): ...
    
    def __init__(self, **kwargs):
        self.__focus_event = Event()
        self.__blur_event = Event()
        self.__input_key_event = EventKwargs()
        self.__press_enter_event = Event()
    
        self._selected: bool = False  
        self._selected_clear_pixel: Union[Pixel, None] = Converter.toPixel(kwargs.get('selected_clear_pixel'))
        
        super().__init__(**kwargs)
    
    def inputKey(self, key: str) -> bool:
        if key is Keys.ENTER and len(self.press_enter_event) > 0:
            self.press_enter_event.invoke()
            return True
        return False
    
    def getClearPixel(self):
        return self.selected_clear_pixel if self.selected else super().getClearPixel()
    
    @property
    def selected(self) -> bool:
        return self._selected
    @selected.setter
    def selected(self, value: bool):
        if value != self._selected:
            self._selected = value
            (self.focus_event if self.selected else self.blur_event).invoke()
            self.setFlagRefresh()
    
    @property
    def selected_clear_pixel(self) -> Union[Pixel, None]:
        return self._selected_clear_pixel
    @selected_clear_pixel.setter
    def selected_clear_pixel(self, value: Union[Pixel, None]):
        self._selected_clear_pixel = value
        self.setFlagRefresh()
    
    @property
    def focus_event(self) -> Event:
        return self.__focus_event
    @property
    def blur_event(self) -> Event:
        return self.__blur_event
    @property
    def input_key_event(self) -> EventKwargs:
        '''
            func(key: str) -> None
        '''
        return self.__input_key_event
    @property
    def press_enter_event(self) -> Event:
        return self.__press_enter_event