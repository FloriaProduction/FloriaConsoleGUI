from typing import Union, Iterable

from ..Widget import Widget
from ..Pixel import Pixel
from ...Classes import Vec2, Vec3
from ..Drawer import Drawer
from ... import Converter
from ... import Func

class Container(Widget):
    def __init__(
        self, 
        size: Union[Vec2[int], Iterable[int]] = None, 
        auto_size: bool = False,
        offset_pos: Union[Vec3[int], Iterable[int]] = None, 
        clear_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str, None] = None,
        name: Union[str, None] = None,
        widgets: Union[Iterable[Widget], Widget] = None, 
        *args, **kwargs
    ):
        super().__init__(size, offset_pos, clear_pixel, name, *args, **kwargs)
        
        self._auto_size = auto_size
        self._indent_size = Vec2(0, 0)
        
        self._offset_pos_widgets: Vec3[int] = Vec3(0, 0, 0)
        self._widgets: list[Widget] = []
        for widget in Converter.toListWidgets(widgets):
            self.addWidget(widget)
                
        self._flag_update_auto_size = self._auto_size

    def addWidget(self, widget: Widget):
        self._widgets.append(widget)
        widget.set_refresh_event.add(self.setRefresh)
        if self._auto_size:
            widget.resize_event.add(self.setAutoSize)
    
    def setAutoSize(self):
        self._flag_update_auto_size = True
        self.setRefresh()
    
    def _updateAutoSize(self):
        if self._auto_size is False or len(self._widgets) == 0:
            return
        self.size = Func.calculateSizeByItems(self._widgets) + self._indent_size
        
        self._flag_update_auto_size = False
        
    def refresh(self):
        widgets: list[tuple[str, any]] = []
        for widget in sorted(self._widgets, key=lambda widget: widget.offset_pos.z):
            widgets.append((
                (widget.offset_pos + self._offset_pos_widgets).toTuple()[:2], 
                widget.render()
            ))
        
        if self._flag_update_auto_size:
            self._updateAutoSize()
        
        super().refresh()
        for widget in widgets:
            self._buffer.paste(
                *widget[0],
                widget[1]
            )
