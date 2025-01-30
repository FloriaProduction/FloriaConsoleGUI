from typing import Union, Iterable

from ..Graphic.Pixel import Pixel
from ..Graphic.Windows import Window
from ..Classes import *
from .KeyboardManager import KeyboardManager
from .. import Func


class WindowManager:
    _window_queue: list[Window] = []
    _index_current_window: int = 0
        
    @classmethod
    def openNewWindow(cls, window: Window, switch_current_window: bool = True):
        if window.name is not None and cls.getByName(window.name) is not None:
            raise ValueError(
                f'Window name "{window.name}" already used'
            )
        
        cls._window_queue.append(window)
        if switch_current_window:
            cls._index_current_window = len(cls._window_queue) - 1
        
        window.open_event.invoke()
    
    @classmethod
    def closeCurrentWindow(cls):
        cls._window_queue.pop(cls._index_current_window).close_event.invoke()
        if len(cls._window_queue) > 0:
            cls._normalizeIndexCurrentWindow()
    
    @classmethod
    def closeAll(cls, except_names: Iterable[str] = []):
        windows = cls._window_queue[::-1].copy()
        
        for window in windows:
            if window.name in except_names:
                continue
            window.close_event.invoke()
            cls._window_queue.remove(window)
    
    @classmethod
    def getByName(cls, name: str) -> Union[Window, None]:
        for window in cls._window_queue:
            if window.name == name:
                return window
    
    @classmethod
    def getCurrent(cls) -> Union[Window, None]:
        '''
            if count(windows) == 0
                return `None`
            else
                return `windows[index_current_window]`
        '''
        if len(cls._window_queue) == 0:
            return None
        
        cls._normalizeIndexCurrentWindow()
        
        return cls._window_queue[cls._index_current_window]
    
    @classmethod
    def nextCurrent(cls):
        if len(cls._window_queue) == 0:
            return None
        cls._index_current_window += 1
        cls._normalizeIndexCurrentWindow()
    
    @classmethod
    async def render(cls) -> Union[Buffer[Pixel], None]:
        '''
            if count(windows) == 0
                return `None`
            else
                return `Buffer[Pixel]`
        '''
        
        if len(cls._window_queue) == 0:
            return None
        
        size, offset = Func.calculateSizeByItems(cls._window_queue)
        
        buffer = Buffer(
            *size,
            Pixel.empty
        )
        
        for window in sorted(cls._window_queue, key=lambda window: window.offset_z):
            buffer.paste(
                window.offset_x + offset.x,
                window.offset_y + offset.y,
                await window.render()
            )
        
        return buffer
    
    @classmethod
    def inputKey(cls, key: str, **kwargs):       
        window_current = cls.getCurrent()
        if window_current is None:
            return
        
        match key:
            case Keys.TAB:
                cls.nextCurrent()
            
            case _:
                window_current.inputKey(key)
        
    @classmethod
    def _normalizeIndexCurrentWindow(cls):
        cls._index_current_window = Func.normalizeIndex(cls._index_current_window, len(cls._window_queue))
    
KeyboardManager.pressed_event.add(
    WindowManager.inputKey
)
