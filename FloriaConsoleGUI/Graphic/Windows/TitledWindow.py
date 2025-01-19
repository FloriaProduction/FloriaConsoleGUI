from typing import Union, Iterable

from .Window import Window
from ..Widgets.Widget import Widget
from ..Pixel import Pixel
from ...Classes import Vec3, Vec2, Vec4, Buffer, Anchor, Orientation
from ... import Func
from ... import Converter
from ..Drawer import Drawer


class TitledWindow(Window):
    def __init__(
            self,
            size: Union[Vec2[int], Iterable[int]] = None,
            min_size: Union[Vec2[Union[int, None]], Iterable[Union[int, None]], None] = None,
            max_size: Union[Vec2[Union[int, None]], Iterable[Union[int, None]], None] = None,
            padding: Union[Vec4[int], Iterable[int]] = None,
            auto_size: bool = False,
            offset_pos: Union[Vec3[int], Iterable[int]] = None, 
            clear_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str] = None,
            name: Union[str, None] = None,
            widgets: Union[Iterable[Widget], Widget] = [], 
            direction: Union[Orientation, None] = Orientation.horizontal,
            gap: int = 0,
            can_be_moved: bool = True,
            frame: bool = False,
            frame_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str] = None,
            title: str = 'unnamed',
            title_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str] = None,
            title_anchor: Union[Anchor, str] = Anchor.center, 
            title_style: int = 0,
            *args, **kwargs
        ):
        '''
            title_style: `int` = 0 | 1
        '''
        
        super().__init__(
            size=size, 
            min_size=min_size,
            max_size=max_size,
            padding=padding,
            auto_size=auto_size,
            offset_pos=offset_pos, 
            clear_pixel=clear_pixel, 
            name=name, 
            widgets=widgets,
            direction=direction,
            gap=gap,
            can_be_moved=can_be_moved,
            frame=frame,
            frame_pixel=frame_pixel,
            *args, **kwargs
        )
                
        self._title = title
        self._title_pixel = Converter.toPixel(title_pixel, Pixel((0, 0, 0), (255, 255, 255)))
        self._title_anchor = Converter.toAnchor(title_anchor)
        self._title_buffer: Buffer[Pixel] = Buffer.empty
        self._title_style = title_style
        
        self._flag_renderTitle = True
        
        self.resize_event.add(self.setFlagRenderTitle)
        

    def setFlagRenderTitle(self):
        self._flag_renderTitle = True
        self.setFlagRefresh()
    
    async def renderTitle(self) -> Buffer[Pixel]:        
        match self._title_style:
            case 1:
                buffer = Buffer(
                    self.width + self.padding.horizontal,
                    3,
                    self.clear_pixel
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
                    await Drawer.renderTextBuffer(
                        Func.setTextAnchor(
                            self._title,
                            self._title_anchor,
                            max(self.width + self.padding.horizontal - 2, 0),
                            crop=True
                        ),
                        self._title_pixel
                    ),
                    Vec4(1, 1, 1, 1),
                )
            
            case _:
                buffer = Buffer(
                    self.width,
                    1,
                    self.clear_pixel,
                    [
                        Pixel.changePixel(self._title_pixel, part) for part in Func.setTextAnchor(
                            self._title, 
                            self._title_anchor, 
                            self.width + self.padding.horizontal, 
                            crop=True
                        )
                    ]
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
