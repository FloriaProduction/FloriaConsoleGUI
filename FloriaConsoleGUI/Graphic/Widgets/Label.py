from typing import Union, Iterable

from ...Classes import Vec2, Vec3, Vec4, Event, Buffer, Anchor
from .Widget import Widget
from ..Pixel import Pixel
from ... import Converter
from ... import Func
from ..Drawer import Drawer


class Label(Widget):
    def __init__(
        self, 
        text: str = 'Label',
        text_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str, None] = None,
        text_anchor: Anchor = Anchor.left,
        text_max_size: Union[Vec2[int], Iterable[int]] = None,
        size: Union[Vec2[int], Iterable[int]] = None,
        min_size: Union[Vec2[Union[int, None]], Iterable[Union[int, None]], None] = None,
        max_size: Union[Vec2[Union[int, None]], Iterable[Union[int, None]], None] = None,
        padding: Union[Vec4[int], Iterable[int]] = None,
        offset_pos: Union[Vec3[int], Iterable[int]] = None, 
        clear_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str] = None,
        name: Union[str, None] = None,
        can_be_moved: bool = True,
        *args, **kwargs
        ):
        super().__init__(
            size=size, 
            min_size=min_size,
            max_size=max_size,
            padding=padding, 
            offset_pos=offset_pos, 
            clear_pixel=clear_pixel, 
            name=name, 
            can_be_moved=can_be_moved,
            *args, **kwargs
        )
        self._change_text_event = Event()
        
        self._text = Converter.toMultilineText(text)
        self._text_pixel = text_pixel
        self._text_anchor = Converter.toAnchor(text_anchor)
        self._text_max_size = Converter.toVec2(text_max_size, Vec2(None, None), True)
    
    async def renderTextBuffer(self, add_empty_symbol_to_end: bool = False) -> Buffer[Pixel]:
        text_buffer = await Drawer.renderTextBuffer(
            self.text + (' ' if add_empty_symbol_to_end else ''),
            Func.choisePixel(self.text_pixel, self.clear_pixel)
        )
        
        return text_buffer

    async def refresh(self):
        text_buffer = await self.renderTextBuffer()
        
        self.size = text_buffer.size
        
        await super().refresh()
        
        self._buffer.pasteByAnchor(
            0, 0,
            text_buffer,
            self.text_anchor,
            self.padding
        )
    
    def setText(self, value: str):
        lines = [
            line[:(len(line) if self.text_max_size.width is None else self.text_max_size.width)] 
            for line in value.split('\n')
        ]
        self._text = '\n'.join(lines[:(len(lines) if self.text_max_size.height is None else self.text_max_size.height)])
        self._change_text_event.invoke()
        self.setFlagRefresh()
    def getText(self) -> str:
        return self._text
    @property
    def text(self) -> str:
        return self.getText()
    @text.setter
    def text(self, value: str):
        self.setText(value)

    def getTextPixel(self) -> Union[Pixel, None]:
        return self._text_pixel
    def setTextPixel(self, value: Union[Pixel, None]):
        self._text_pixel = value
    @property
    def text_pixel(self) -> Union[Pixel, None]:
        return self.getTextPixel()
    @text_pixel.setter
    def text_pixel(self, value: Union[Pixel, None]):
        self._text_pixel = value
    
    @property
    def text_anchor(self) -> Anchor:
        return self._text_anchor
    @text_anchor.setter
    def text_anchor(self, value: Anchor):
        self._text_anchor = value
    
    @property
    def text_max_size(self) -> Vec2[Union[int, None]]:
        return self._text_max_size
    @text_max_size.setter
    def text_max_size(self, value: Vec2[Union[int, None]]):
        self._text_max_size = value
        
    @property
    def change_text_event(self) -> Event:
        return self._change_text_event