from typing import Union, Iterable, Callable

from ...Classes import Vec2, Vec3, Vec4, Event, Anchor, Keys
from ..Pixel import Pixel
from .InteractiveWidget import InteractiveWidget


class Button(InteractiveWidget):
    def __init__(
        self,
        text: str = 'Button',
        text_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str] = None,
        text_anchor: Anchor = Anchor.center,
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
        on_press_functions: Union[Iterable[Callable[[], None]], Callable[[], None]] = [],
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
            tabindex=tabindex, 
            select_clear_pixel=select_clear_pixel, 
            can_be_moved=can_be_moved,
            *args, **kwargs
        )
        self._pressed_event = Event(
            *(on_press_functions if isinstance(on_press_functions, Iterable) else [on_press_functions])
        )
        
    def inputKey(self, key) -> bool:
        match key:
            case Keys.ENTER:
                self.pressed_event.invoke()

            case _:
                return False
        return True
    
    @property
    def pressed_event(self) -> Event:
        return self._pressed_event