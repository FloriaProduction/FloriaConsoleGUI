from typing import Union, Iterable

from ..Graphic.Pixel import Pixel
from ..Graphic.Windows import Window
from ..Classes import Buffer
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
    async def render(cls) -> Union[Buffer[Pixel], None]:
        '''
            if count(windows) == 0
                return `None`
            else
                return `Buffer[Pixel]`
        '''
        
        if len(cls._window_queue) == 0:
            return None

        windows: list[tuple[any]] = [
            ((window.offset_pos.x, window.offset_pos.y), await window.render()) for window in sorted(cls._window_queue, key=lambda window: window.offset_z)
        ]
        
        buffer = Buffer(*Func.calculateSizeByItems(cls._window_queue), Pixel.empty)
        
        for window in windows:
            buffer.paste(*window[0], window[1])
        
        return buffer
    
    @classmethod
    def press(cls, key: str, **kwargs):       
        window_current = cls.getCurrent()
        if window_current is None:
            return
        
        window_current.inputKey(key)
        
    @classmethod
    def _normalizeIndexCurrentWindow(cls):
        cls._index_current_window = Func.normalizeIndex(cls._index_current_window, len(cls._window_queue))
    
KeyboardManager.pressed_event.add(
    WindowManager.press
)
