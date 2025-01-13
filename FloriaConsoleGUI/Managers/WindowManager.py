from typing import Union
import sys

from ..Graphic import Pixel, Pixels
from ..Graphic.Widgets import Widget
from ..Graphic.Windows import Window
from ..Classes import Buffer, Vec2, Anchor, Orientation
from ..Log import Log
from ..GVars import GVars
from .KeyboardManager import KeyboardManager, posix_key
from .. import Func

class WindowManager:
    _window_queue: list[Window] = []
    _index_current_window: int = 0
        
    @classmethod
    def openNewWindow(cls, window: Window, switch_current_window: bool = True):
        if window.name is not None and cls.getByName(window.name) is not None:
            raise ValueError(f'Window name "{window.name}" already used')
        
        cls._window_queue.append(window)
        if switch_current_window:
            cls._index_current_window = len(cls._window_queue) - 1
        
        window.open_event.invoke()
    
    @classmethod
    def closeCurrentWindow(cls):
        cls._window_queue.pop(cls._index_current_window).close_event.invoke()
        cls._normalizeIndexCurrentWindow()
    
    @classmethod
    def closeAll(cls):       
        for window in cls._window_queue[::-1]:
            window.close_event.invoke()
        cls._window_queue.clear()
    
    @classmethod
    def getByName(cls, name: str) -> Union[Window, None]:
        for window in cls._window_queue:
            if window.name == name:
                return window
    
    @classmethod
    def getCurrent(cls) -> Union[Window, None]:
        if len(cls._window_queue) == 0:
            return None
        
        cls._normalizeIndexCurrentWindow()
        
        return cls._window_queue[cls._index_current_window]
    
    @classmethod
    def render(cls) -> Union[Buffer[Pixel], None]:
        if len(cls._window_queue) == 0:
            return None

        windows: list[tuple[any]] = [
            ((window.offset_pos.x, window.offset_pos.y), window.render()) for window in sorted(cls._window_queue, key=lambda window: window.offset_z)
        ]
        
        buffer = Buffer(*Func.calculateSizeByItems(cls._window_queue), Pixel.empty)
        
        for window in windows:
            buffer.paste(*window[0], window[1])
        
        return buffer

    @classmethod
    def pressed(cls, char: str, **kwargs):       
        window_current = cls.getCurrent()
        if window_current is None:
            return
        
        match char:
            case '\x00H':
                window_current.selectBackWidget()
            case '\x00P':
                window_current.selectNextWidget()
        
    @classmethod
    def _normalizeIndexCurrentWindow(cls):
        if len(cls._window_queue) == 0:
            return

        if cls._index_current_window < 0:
            cls._index_current_window = 0
        elif cls._index_current_window >= len(cls._window_queue):
            cls._index_current_window = len(cls._window_queue) - 1
    
KeyboardManager.addHandlerToPressedEvent(WindowManager.pressed)
