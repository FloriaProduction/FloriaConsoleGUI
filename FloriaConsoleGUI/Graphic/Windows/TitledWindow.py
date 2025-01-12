from typing import Union, Iterable

from ..Window import Window
from ..Widget import Widget
from ..Pixel import Pixel
from ...Classes import Vec3, Vec2, Buffer, Anchor
from ... import Func
from ... import Converter
from ..Drawer import Drawer


class TitledWindow(Window):
    def __init__(
            self,
            size: Union[Vec2[int], Iterable[int]] = None, 
            offset_pos: Union[Vec3[int], Iterable[int]] = None, 
            widgets: Union[Iterable[Widget], Widget] = None, 
            clear_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str] = None,
            frame: bool = False,
            name: Union[str, None] = None,
            title: str = 'unnamed',
            title_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str] = None,
            title_anchor: Union[Anchor, str] = Anchor.center, 
            title_style: int = 0,
            *args, **kwargs
        ):
        '''
            title_style: `int` = 0 | 1
        '''
        
        super().__init__(size, offset_pos, widgets, clear_pixel, frame, name, *args, **kwargs)
                
        self._title = title
        self._title_pixel = Converter.toPixel(title_pixel, Pixel((0, 0, 0), (255, 255, 255)))
        self._title_anchor = Converter.toAnchor(title_anchor)
        self._title_buffer: Buffer[Pixel] = Buffer.empty
        self._title_style = title_style
        
        self.resize_event.add(self.setRenderTitle)
        
        self._flag_renderTitle = True

    def setRenderTitle(self):
        self._flag_renderTitle = True
    
    def renderTitle(self):
        match self._title_style:
            case 1:
                self._title_buffer = Drawer.frame(
                    self.width, 3, 
                    self._clear_pixel.front_color, 
                    self._clear_pixel.back_color
                )
                title_tex_length = max(self.width - 2, 0)
                self._title_buffer.paste(
                    1, 1,
                    Buffer(
                        title_tex_length, 1,
                        self._title_pixel,
                        [
                            Pixel.changePixel(self._title_pixel, part) for part in Func.setTextAnchor(self._title, self._title_anchor, title_tex_length)[:title_tex_length]
                        ]
                    )
                )
            
            case _:
                self._title_buffer = Buffer(
                    self.width, 1, 
                    self._title_pixel, 
                    [
                        Pixel.changePixel(self._title_pixel, part) for part in Func.setTextAnchor(self._title, self._title_anchor, self.width)[:self.width]
                    ]
                )
        
        self._offset_pos_widgets = Vec3(
            0, 
            max(self._title_buffer.height-1, 0), 
            0
        )
        self.setUpdateAutoSize()
        
        self._flag_renderTitle = False

    def render(self):
        self._offset_pos_widgets = Vec3(0, 2 if self._title_style == 1 else 0, 0)
        
        buffer = super().render()
        
        if self._flag_renderTitle:
            self.renderTitle()
        
        buffer.paste(0, 0, self._title_buffer, Drawer.mergeFramePixels)
        
        return buffer
    
    @property
    def title(self) -> str:
        return self._title
    @title.setter
    def title(self, value: str):
        self._title = value
        self.setRenderTitle()
