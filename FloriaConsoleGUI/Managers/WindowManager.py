from typing import Union
import sys

from ..Graphic import Window, Pixel, Pixels, Widget
from ..Classes import Buffer, Vec2, Anchor, Orientation
from ..Log import Log
from ..GVars import GVars

class WindowManager:
    _window_queue: list[Window] = []
    
    _buffer_size: Vec2 = Vec2(0, 0)
    _buffer: Union[Buffer[Pixel], None] = None
    
    @classmethod
    def new(cls, window: Window):
        cls._window_queue.append(window)
        cls._update_buffer_size()
        window._open_event.invoke()
    
    @classmethod
    def close(cls):
        cls._window_queue.pop()._close_event.invoke()
    
    @classmethod
    def closeAll(cls):
        for window in cls._window_queue:
            window._close_event.invoke()
        cls._window_queue.clear()
    
    @classmethod
    def getByName(cls, name: str) -> Union[Window, None]:
        return Window.getWindow(name)
    
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
    
    @classmethod
    def render(cls) -> Union[Buffer[Pixel], None]:
        if len(cls._window_queue) == 0:
            if GVars.DEBUG_STOP_RENDER_WHEN_WITHOUT_WINDOWS:
                return None
            return cls._buffer if cls._buffer is not None else Buffer(*cls._buffer_size, Pixel.empty)
    
        cls._update_buffer_size()
        
        cls._buffer = Buffer(*cls._buffer_size, Pixel.empty)
        
        for window in sorted(cls._window_queue, key=lambda window: window.offset_z, reverse=True):
            cls._buffer.paste(window.offset_pos.x, window.offset_pos.y, window.render())
        
        return cls._buffer



    

            
        
        
        
        