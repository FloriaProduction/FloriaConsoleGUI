from typing import Union, Iterable

from ..Widget import Widget
from ..Pixel import Pixel
from ...Classes import Vec2, Vec3
from ..Drawer import Drawer
from ... import Converter

class Container(Widget):
    def __init__(
        self, 
        size: Union[Vec2[int], Iterable[int]] = None, 
        offset_pos: Union[Vec3[int], Iterable[int]] = None, 
        clear_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str, None] = None,
        name: Union[str, None] = None,
        widgets: Union[Iterable[Widget], Widget] = None, 
        *args, **kwargs
    ):
        super().__init__(size, offset_pos, clear_pixel, name, *args, **kwargs)
        
        self._widgets: list[Widget] = Converter.toListWidgets(widgets)
        self._offset_widgets: Vec3[int] = Vec3(0, 0, 0)

        for widget in self._widgets:
            widget.set_refresh_event.add(lambda: self.setRefresh())
        
    def refresh(self):
        super().refresh()
        
        for widget in sorted(self._widgets, key=lambda widget: widget.offset_pos.z):
            self._buffer.paste(
                *((widget.offset_pos + self._offset_widgets).toTuple()[:2]), 
                widget.render(), 
                Drawer.mergeFramePixels
            )
