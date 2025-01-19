from typing import Union, Iterable

from ...Classes import Vec2, Vec3, Vec4, Event, Buffer, Keys, Anchor
from .InteractiveWidget import InteractiveWidget
from ..Pixel import Pixel, Pixels
from ... import Converter
from ... import Func


class TextBox(InteractiveWidget):
    def __init__(
        self, 
        text: str = 'TextBox',
        text_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str, None] = None,
        text_anchor: Anchor = Anchor.left,
        text_max_size: Union[Vec2[int], Iterable[int]] = None,
        caret_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str, None] = None,
        size: Union[Vec2[int], Iterable[int]] = None,
        min_size: Union[Vec2[Union[int, None]], Iterable[Union[int, None]], None] = None,
        max_size: Union[Vec2[Union[int, None]], Iterable[Union[int, None]], None] = None,
        padding: Union[Vec4[int], Iterable[int]] = None,
        offset_pos: Union[Vec3[int], Iterable[int]] = None, 
        clear_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str] = None,
        name: Union[str, None] = None,
        tabindex: Union[int, None] = None,
        select_clear_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str] = None,
        can_be_moved: bool = True,
        *args, **kwargs
    ):
        super().__init__(
            text=text,
            text_pixel=text_pixel,
            text_anchor=text_anchor,
            size=size,
            min_size=min_size,
            max_size=max_size,
            padding=padding,
            offset_pos=offset_pos,
            clear_pixel=clear_pixel,
            name=name,
            tab_index=tabindex,
            select_clear_pixel=select_clear_pixel,
            can_be_moved=can_be_moved,
            *args, **kwargs
        )
        self._change_caret_event = Event()
        
        self._text_max_size = Converter.toVec2(text_max_size, Vec2(None, None), True)
        self._caret = 0
        self._caret_pixel = Converter.toPixel(caret_pixel, Pixels.black_white)
    
    async def renderTextBuffer(self) -> Buffer[Pixel]:
        text_buffer = await super().renderTextBuffer(True)
        
        if text_buffer.width > 0 and text_buffer.height > 0 and self.selected:
            lines = self.text[:self.caret].split('\n')
            
            caret_x, caret_y = len(lines[-1]), len(lines) - 1
            
            text_buffer[caret_x, caret_y] = Pixel.changePixel(
                text_buffer[caret_x, caret_y], 
                front_color=self.caret_pixel.front_color, 
                back_color=self.caret_pixel.back_color
            )
        
        return text_buffer
    
    def pasteText(self, symbol: chr):
        lines = self.text.split('\n')
        lines_slice = self.text[:self.caret].split('\n')
        line_width = len(lines[len(lines_slice)-1])
        line_height = len(lines)
        
        # добавить проверку text на multiline
        if (self.text_max_size.width is not None and line_width >= self.text_max_size.width and '\n' not in symbol) or \
            (self.text_max_size.height is not None and line_height >= self.text_max_size.height and '\n' in symbol):
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
        break_word_symbols = [' ', '\n']
        
        match key:
            case Keys.LEFT | Keys.CTRL_LEFT:
                self.caret -= 1
                
                if key == Keys.CTRL_LEFT:
                    while 1 <= self.caret < len(self.text) and self.text[self.caret] in break_word_symbols:
                        self.caret -= 1
                        
                    while 1 <= self.caret < len(self.text) and self.text[self.caret] not in break_word_symbols:
                        self.caret -= 1
                    
            case Keys.RIGHT | Keys.CTRL_RIGHT:
                self.caret += 1
                
                if key == Keys.CTRL_RIGHT:
                    while 0 <= self.caret < len(self.text) and self.text[self.caret] in break_word_symbols:
                        self.caret += 1
                    
                    while 0 <= self.caret < len(self.text) and self.text[self.caret] not in break_word_symbols:
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
                
            case Keys.ENTER:
                self.pasteText('\n')

            case _:
                if key.isprintable():
                    self.pasteText(key)
                    
                else:
                    return False
        return True

    def getCaret(self) -> int:
        return self._caret
    def setCaret(self, value: int):        
        text_length = len(self.text) + 1
        self._caret = value - value // text_length * text_length
        self._change_caret_event.invoke()
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
        
    @property
    def caret_pixel(self) -> Union[Pixel, None]:
        return self.getCaretPixel()
    @caret_pixel.setter
    def caret_pixel(self, value: Union[Pixel, None]):
        self.setCaretPixel(value)
    
    @property
    def change_caret_event(self) -> Event:
        return self._change_caret_event

