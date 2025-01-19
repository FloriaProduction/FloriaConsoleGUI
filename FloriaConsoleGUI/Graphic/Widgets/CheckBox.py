from typing import Union, Callable, Iterable

from ...Classes import Vec2, Vec3, Vec4, Anchor, Event
from ..Pixel import Pixel
from .Button import Button
from ... import Converter
from ... import Func


class CheckBox(Button):
    def __init__(
        self, 
        text: str = 'CheckBox', 
        checked_text: Union[str, None] = None,
        text_pixel: Pixel | tuple[Vec3[int] | Iterable[int], Vec3[int] | Iterable[int], str] | str = None, 
        text_anchor: Anchor = Anchor.center, 
        text_max_size: Union[Vec2[int], Iterable[int]] = None,
        checked: bool = False,
        checked_pixel: Pixel | tuple[Vec3[int] | Iterable[int], Vec3[int] | Iterable[int], str] | str = None,
        select_checked_pixel: Pixel | tuple[Vec3[int] | Iterable[int], Vec3[int] | Iterable[int], str] | str = None,
        size: Vec2[int] | Iterable[int] = None, 
        min_size: Union[Vec2[Union[int, None]], Iterable[Union[int, None]], None] = None,
        max_size: Union[Vec2[Union[int, None]], Iterable[Union[int, None]], None] = None,
        padding: Vec4[int] | Iterable[int] = None, 
        offset_pos: Vec3[int] | Iterable[int] = None, 
        clear_pixel: Pixel | tuple[Vec3[int] | Iterable[int], Vec3[int] | Iterable[int], str] | str = None, 
        name: str | None = None, 
        tabindex: int | None = None, 
        select_clear_pixel: Pixel | tuple[Vec3[int] | Iterable[int], Vec3[int] | Iterable[int], str] | str = None, 
        on_press_functions: Iterable[Callable[[], None]] | Callable[[], None] = [], 
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
            on_press_functions=on_press_functions, 
            can_be_moved=can_be_moved,
            *args, **kwargs
        )

        self._checked_text = Converter.toText(checked_text)
        self._change_checked_event = Event()
    
        self._checked: bool = checked
        self._checked_pixel = Converter.toPixel(checked_pixel)
        self._select_checked_pixel = Converter.toPixel(select_checked_pixel)
        
        self.pressed_event.add(self.switchChecked)
        
    def getClearPixel(self) -> Pixel | None:
        return Func.choisePixel(
            (self.select_checked_pixel if self.selected else self.checked_pixel) if self.checked else None, 
            super().getClearPixel()
        )
    
    def getText(self) -> str:
        return self.checked_text if self.checked else super().getText()
    
    def getChecked(self) -> bool:
        return self._checked
    def setChecked(self, value: bool):
        self._checked = value
        self.setFlagRefresh()
    def switchChecked(self):
        self.checked = not self.checked
            
    @property
    def checked(self) -> bool:
        return self.getChecked()
    @checked.setter
    def checked(self, value: bool):
        self.setChecked(value)
    
    @property
    def checked_pixel(self) -> Union[Pixel, None]:
        return self._checked_pixel
    @checked_pixel.setter
    def checked_pixel(self, value: Union[Pixel, None]):
        self._checked_pixel = value
        self.setFlagRefresh()
    
    @property
    def select_checked_pixel(self) -> Union[Pixel, None]:
        return self._select_checked_pixel
    @select_checked_pixel.setter
    def select_checked_pixel(self, value: Union[Pixel, None]):
        self._select_checked_pixel = value
        self.setFlagRefresh()
        
    @property
    def change_checked_event(self) -> Event:
        return self._change_checked_event
    
    @property
    def checked_text(self) -> str:
        return self._checked_text
    @checked_text.setter
    def checked_text(self, value: str):
        self._checked_text = Converter.toText(value)
        self.setFlagRefresh()