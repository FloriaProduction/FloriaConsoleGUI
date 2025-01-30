from typing import Union, Iterable, overload, Callable

from .Label import Label
from .InteractiveWidget import InteractiveWidget
from ..Pixel import *
from ...Classes import *
from ..Drawer import Drawer
from ... import Converter
from ... import Func


class Button(InteractiveWidget, Label):
    @overload
    def __init__(
        self,
        text: str = 'Button',
        text_anchor: Anchor = Anchor.center,
        text_pixel: Union[Pixel, tuple[Iterable[int], Iterable[int], str], str] = None,
        min_size: Union[Iterable[Union[int, None]], None] = None,
        max_size: Union[Iterable[Union[int, None]], None] = None,
        size_hint: Union[Iterable[Union[float, None]], None] = None,
        padding: Union[Iterable[int]] = None,
        offset_pos: Union[Iterable[int]] = None, 
        pos_hint: dict[str, Union[int, None]] = {},
        clear_pixel: Union[Pixel, tuple[Iterable[int], Iterable[int], str], str] = Pixels.b_gray,
        selected_clear_pixel: Union[Pixel, tuple[Iterable[int], Iterable[int], str], str] = Pixels.black_white,
        name: Union[str, None] = None,
        press_functions: Iterable[Callable[[], None]] = [],
        **kwargs
    ): ...
    
    def __init__(self, **kwargs):      
        kwargs.update({
            'text': kwargs.get('text', 'Button'),
            'text_anchor': kwargs.get('text_anchor', Anchor.center),
            'clear_pixel': kwargs.get('clear_pixel', Pixels.b_gray),
            'selected_clear_pixel': kwargs.get('selected_clear_pixel', Pixels.black_white),  
        })
        super().__init__(**kwargs)
        
        press_functions = kwargs.get('press_functions', [])
        self.press_enter_event.add(
            *(press_functions if isinstance(press_functions, Iterable) else [press_functions])
        )
        
        self.focus_event.add(
            self.refreshTextBuffer
        )   
        self.blur_event.add(
            self.refreshTextBuffer
        )
    
