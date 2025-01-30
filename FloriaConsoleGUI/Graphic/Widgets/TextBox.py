from typing import Union, Iterable, overload

from .Label import Label 
from .InteractiveWidget import InteractiveWidget
from ..Pixel import *
from ...Classes import *
from ..Drawer import Drawer
from ... import Converter
from ... import Func

class TextBox(InteractiveWidget, Label):
    @overload
    def __init__(
        self,
        text: str = 'TextBox',
        text_anchor: Anchor = Anchor.left,
        text_pixel: Union[Pixel, tuple[Iterable[int], Iterable[int], str], str] = None,
        placeholder: str = '',
        placeholder_pixel: Union[Pixel, tuple[Iterable[int], Iterable[int], str], str] = Pixels.f_dark_gray,
        min_size: Union[Iterable[Union[int, None]], None] = None,
        max_size: Union[Iterable[Union[int, None]], None] = None,
        size_hint: Union[Iterable[Union[float, None]], None] = None,
        padding: Union[Iterable[int]] = None,
        offset_pos: Union[Iterable[int]] = None, 
        pos_hint: dict[str, Union[int, None]] = {},
        clear_pixel: Union[Pixel, tuple[Iterable[int], Iterable[int], str], str] = None,
        selected_clear_pixel: Union[Pixel, tuple[Iterable[int], Iterable[int], str], str] = None,
        name: Union[str, None] = None,
        caret_pixel: Union[Pixel, tuple[Iterable[int], Iterable[int], str], str] = Pixels.black_white,
        **kwargs
    ): ...
    
    def __init__(self, **kwargs):
        self._placeholder = kwargs.get('placeholder', '')
        self._placeholder_pixel = kwargs.get('placeholder_pixel', Pixels.f_dark_gray)
        
        self.__change_caret_event = Event()
        
        self._caret = 0
        self._caret_pixel = Converter.toPixel(kwargs.get('caret_pixel'), default=Pixels.black_white)
        
        kwargs.update({
            'text': kwargs.get(
                'text', 
                'TextBox' if self._placeholder == '' else ''
            )
        })
        super().__init__(**kwargs)
        
        self.focus_event.add(
            self.refreshTextBuffer
        )
        self.blur_event.add(
            self.refreshTextBuffer
        )
        self.press_enter_event.add(
            lambda: self.pasteText('\n')
        )
        
        self.break_symbols: list[chr] = [' ', '\n', ';', ',', '.', '/', '\\', '(', ')', '{', '}', '[', ']']
        
    def refreshTextBuffer(self):      
        if len(self.text) > 0:
            super().refreshTextBuffer(True)
        else:
            self._text_buffer = Drawer.renderTextBuffer(
                self.placeholder, 
                self.placeholder_pixel
            )
            self._text_buffer = self._text_buffer.cropBySize(
                0, 0,
                self.max_size.width if self.max_size.width is not None else self._text_buffer.width,
                self.max_size.height if self.max_size.height is not None else self._text_buffer.height,
            )
            self.size = self._text_buffer.size
            
        if self._text_buffer.width > 0 and self._text_buffer.height > 0 and self.selected:
            lines = self.text[:self.caret].split('\n')
            
            caret_x, caret_y = min(self._text_buffer.width-1, max(0, len(lines[-1]))), min(self._text_buffer.height - 1, max(0, len(lines) - 1))
            caret_pixel = Func.choisePixel(self.caret_pixel, default=Pixels.black_white)
            
            self._text_buffer[caret_x, caret_y] = Pixel.changePixel(
                self._text_buffer[caret_x, caret_y], 
                front_color=caret_pixel.front_color, 
                back_color=caret_pixel.back_color
            )

    def pasteText(self, symbol: chr):
        lines = self.text.split('\n')
        lines_slice = self.text[:self.caret].split('\n')
        line_width = len(lines[len(lines_slice)-1])
        line_height = len(lines)
        
        # добавить проверку text на multiline
        if (self.max_size.width is not None and line_width >= self.max_size.width and '\n' not in symbol) or \
            (self.max_size.height is not None and line_height >= self.max_size.height and '\n' in symbol):
            return
        
        self.text = self.text[:self.caret] + symbol + self.text[self.caret:]
        self.caret += len(symbol)
    
    def deleteSymbol(self, move_caret: bool, count: int = 1):
        if move_caret and self.caret > 0:
            self.caret -= 1
        
        self.text = self.text[:self.caret] + self.text[self.caret + 1:]
        if count > 1:
            self.deleteSymbol(move_caret, count-1)
    
    def inputKey(self, key: str) -> bool:
        match key:
            case Keys.LEFT | Keys.CTRL_LEFT:
                self.caret -= 1
                
                if key == Keys.CTRL_LEFT:
                    while 1 <= self.caret < len(self.text) and self.text[self.caret] in self.break_symbols:
                        self.caret -= 1
                        
                    while 1 <= self.caret < len(self.text) and self.text[self.caret] not in self.break_symbols:
                        self.caret -= 1
                    
            case Keys.RIGHT | Keys.CTRL_RIGHT:
                self.caret += 1
                
                if key == Keys.CTRL_RIGHT:
                    while 0 <= self.caret < len(self.text) and self.text[self.caret] in self.break_symbols:
                        self.caret += 1
                    
                    while 0 <= self.caret < len(self.text) and self.text[self.caret] not in self.break_symbols:
                        self.caret += 1
            
            case Keys.BACKSPACE | Keys.CTRL_BACKSPACE:
                self.deleteSymbol(True)
                
                if key == Keys.CTRL_BACKSPACE:
                    pass
                
            case Keys.DELETE | Keys.CTRL_DELETE:
                self.deleteSymbol(False)
            
            case Keys.HOME:
                self.caret = sum(map(lambda line: len(line) + 1, self.text[:self.caret].split('\n')[:-1]))
            
            case Keys.END:
                # caret = sum( len( lines [:caret] ) ) + len( current line )
                strip_lines = self.text[:self.caret].split('\n')
                self.caret = sum(map(lambda line: len(line) + 1, strip_lines[:-1])) + len(self.text.split('\n')[len(strip_lines)-1])

            case _:
                if key.isprintable():
                    self.pasteText(key)
                    
                else:
                    return super().inputKey(key)
        return True

    def getCaret(self) -> int:
        return self._caret
    def setCaret(self, value: int):        
        text_length = len(self.text) + 1
        self._caret = value - value // text_length * text_length
        self.__change_caret_event.invoke()
        self.refreshTextBuffer()
        self.setFlagRefresh()
    @property
    def caret(self) -> int:
        return self.getCaret()
    @caret.setter
    def caret(self, value: int):
        self.setCaret(value)
        
    def getCaretPixel(self) -> Union[Pixel, None]:
        return Func.choisePixel(self._caret_pixel, self.text_pixel, self.clear_pixel) 
    def setCaretPixel(self, value: Union[Pixel, None]):
        self._caret_pixel = value
        self.refreshTextBuffer()
        
    @property
    def caret_pixel(self) -> Union[Pixel, None]:
        return self.getCaretPixel()
    @caret_pixel.setter
    def caret_pixel(self, value: Union[Pixel, None]):
        self.setCaretPixel(value)
    
    @property
    def placeholder(self) -> str:
        return self._placeholder
    @placeholder.setter
    def placeholder(self, value: str):
        self._placeholder = value
    
    @property
    def placeholder_pixel(self) -> Union[Pixel, None]:
        return self._placeholder_pixel
    @placeholder_pixel.setter
    def placeholder_pixel(self, value: Union[Pixel, None]):
        self._placeholder_pixel = value
    
    @property
    def change_caret_event(self) -> Event:
        return self.__change_caret_event