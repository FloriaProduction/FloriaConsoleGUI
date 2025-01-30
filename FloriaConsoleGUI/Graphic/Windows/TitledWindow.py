from typing import Union, Iterable, overload

from .Window import Window
from ..Widgets.Widget import Widget
from ..Pixel import Pixel, Pixels
from ...Classes import Vec3, Vec2, Vec4, Buffer, Anchor, Orientation
from ... import Func
from ... import Converter
from ..Drawer import Drawer


class TitledWindow(Window):
    @overload
    def __init__(
        self,
        size: Vec2[int] | Iterable[int] = None,
        min_size: Vec2[int | None] | Iterable[int | None] | None = None,
        max_size: Vec2[int | None] | Iterable[int | None] | None = None,
        size_hint: Vec2[float | None] | Iterable[float | None] | None = None,
        padding: Vec4[int] | Iterable[int] = None,
        offset_pos: Vec3[int] | Iterable[int] = None,
        clear_pixel: Pixel | tuple[Vec3[int] | Iterable[int], Vec3[int] | Iterable[int], str] | str = None,
        name: str | None = None,
        widgets: Union[Iterable[Widget], Widget] = [], 
        size_by_objects: bool = False,
        objects_direction: Union[Orientation, None] = None,
        gap: int = 0,
        frame: bool = True,
        frame_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str] = None,
        title: str = 'unnamed',
        title_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str] = None,
        title_anchor: Union[Anchor, str] = Anchor.center, 
        title_style: int = 0,
        **kwargs
    ):
        '''
            title_style: `int` = 0 | 1
        '''
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
                
        self._title = kwargs.get('title', 'unnamed')
        self._title_pixel = Converter.toPixel(kwargs.get('title_pixel'), Pixels.black_white)
        self._title_anchor = Converter.toAnchor(kwargs.get('title_anchor', Anchor.center))
        self._title_buffer: Buffer[Pixel] = Buffer.empty
        self._title_style = kwargs.get('title_style', 0)
        
        self._flag_renderTitle = True
        
        self.resize_event.add(
            self.setFlagRenderTitle
        )
        
    def setFlagRenderTitle(self):
        self._flag_renderTitle = True
        self.setFlagRefresh()
    
    async def renderTitle(self) -> Buffer[Pixel]:  
        text_buffer = Drawer.renderTextBuffer(
            Func.setTextAnchor(
                self._title,
                self._title_anchor,
                max(self.width + self.padding.horizontal - 2, 0),
                crop=True
            ),
            self._title_pixel
        )
              
        match self._title_style:
            case 1:
                buffer = Buffer(
                    self.width + self.padding.horizontal,
                    3,
                    self._title_pixel
                )
                buffer.paste(
                    0, 0,
                    Drawer.frame(
                        *buffer.size,
                        *self.clear_pixel.getColors()
                    )
                )
                buffer.paste(
                    0, 0,
                    text_buffer,
                    Vec4(1, 1, 1, 1),
                )
            
            case _:
                buffer = Buffer(
                    self.width + self.padding.horizontal, 1,
                    self._title_pixel
                )
                
                buffer.paste(
                    0, 0,
                    text_buffer,
                    Vec4(0, 0, 1, 1)
                )
                
        
        self._flag_renderTitle = False
        return buffer
    
    async def refresh(self):
        await super().refresh()
        
        if self._flag_renderTitle:
            self._title_buffer = await self.renderTitle()
        
        self._buffer.paste(
            0, 0,
            self._title_buffer,
            func=Drawer.mergeFramePixels
        )
    
    def getPadding(self):
        return super().getPadding() + Vec4(
            2 if self._title_style == 1 else 0, 
            0, 
            0, 
            0
        )

    @property
    def title(self) -> str:
        return self._title
    @title.setter
    def title(self, value: str):
        self._title = Converter.toText(value)
        self.setFlagRenderTitle()
