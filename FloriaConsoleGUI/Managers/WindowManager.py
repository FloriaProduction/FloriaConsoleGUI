from typing import Union
import sys

from ..Graphic import Window, Pixel, Pixels, Widget
from ..Classes import Buffer, Vec2, Anchor, Orientation
from ..Log import Log
from ..GVars import GVars
from .KeyboardManager import KeyboardManager, posix_key

class WindowManager:
    _window_queue: list[Window] = []
    _index_current_window: int = 0
    
    _buffer_size: Vec2[int] = Vec2(0, 0)
    
    @classmethod
    def openNewWindow(cls, window: Window, switch_current_window: bool = True):
        if window.name is not None and cls.getByName(window.name) is not None:
            raise ValueError(f'Window name "{window.name}" already used')
        
        cls._window_queue.append(window)
        if switch_current_window:
            cls._index_current_window = len(cls._window_queue) - 1
        
        cls._update_buffer_size()
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
    
        cls._update_buffer_size()
        
        buffer = Buffer(*cls._buffer_size, Pixel.empty)
        
        for window in sorted(cls._window_queue, key=lambda window: window.offset_z, reverse=True):
            buffer.paste(window.offset_pos.x, window.offset_pos.y, window.render())
        
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
    
    @classmethod
    def _update_buffer_size(cls):
        max_width = max_height = 0
        for window in cls._window_queue:
            width, height = window.offset_x + window.width, window.offset_y + window.height
            if width > max_width:
                max_width = width
            if height > max_height:
                max_height = height
        cls._buffer_size = Vec2(max_width, max_height)
    
KeyboardManager.addHandlerToPressedEvent(WindowManager.pressed)
