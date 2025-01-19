from typing import Union, Iterable

from ..BaseGraphicObject import BaseGraphicContainerObject
from ..Pixel import Pixel
from ..Drawer import Drawer
from ..Widgets.Widget import Widget
from ..Widgets.InteractiveWidget import InteractiveWidget
from ...Classes import Event, Vec2, Vec3, Vec4, Keys, Orientation

from ... import Converter
from ... import Func


class Window(BaseGraphicContainerObject):    
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
        *args, **kwargs
    ):

        
        super().__init__(
            size=size, 
            min_size=min_size,
            max_size=max_size,
            padding=padding,
            auto_size=auto_size, 
            offset_pos=offset_pos, 
            clear_pixel=Func.choisePixel(clear_pixel, Pixel.empty), 
            name=name, 
            objects=widgets, 
            direction=direction,
            gap=gap,
            can_be_moved=can_be_moved,
        *args, **kwargs)
        
        ''' events '''
        self._open_event = Event()
        self._close_event = Event()
        self._change_frame_pixel_event = Event()
        
        ''' pixels ''' 
        self._frame_pixel = Converter.toPixel(frame_pixel)
        
        ''' interact_objects '''
        self._select_index: int = 0
        self._interact_objects: list[InteractiveWidget] = []
        self.updateInteractWidgets()
        self.add_object_event.add(self.updateInteractWidgets)
        
        ''' other '''
        self._frame = frame
        
    async def refresh(self):
        await super().refresh()
        
        if self.frame:
            frame_pixel: Pixel = Func.choisePixel(
                self.frame_pixel, 
                self.clear_pixel
            )
            
            self._buffer.paste(
                0, 0,
                Drawer.frame(
                    self.width + self.padding.horizontal,
                    self.height + self.padding.vertical,
                    frame_pixel.front_color, 
                    frame_pixel.back_color
                )
            )
        
    def getPadding(self):
        return super().getPadding() + (
            Vec4(1, 1, 1, 1) if self.frame else Vec4(0, 0, 0, 0)
        )
    
    def updateInteractWidgets(self):
        def _f(container_object: BaseGraphicContainerObject) -> list[InteractiveWidget]:
            widgets = []
            for object in container_object:
                if issubclass(object.__class__, BaseGraphicContainerObject):
                    widgets += _f(object)
                
                if issubclass(object.__class__, InteractiveWidget):
                    widgets.append(object)
            return widgets
        
        self._interact_objects = _f(self._objects)
        self.selectWidget(0) 
    
    def _normalizeSelectIndex(self):
        self._select_index = Func.normalizeIndex(self._select_index, len(self._interact_objects))
    
    def getSelectedWidget(self) -> Union[InteractiveWidget, None]:
        if len(self._interact_objects) == 0:
            return None
        self._normalizeSelectIndex()
        return self._interact_objects[self._select_index]
    
    def selectWidget(self, index: int):
        if len(self._interact_objects) == 0:
            return
        
        previous_widget = self.getSelectedWidget()
        if previous_widget is not None:
            previous_widget.selected = False
            
        self._select_index = index
        self._normalizeSelectIndex()
        
        next_widget = self.getSelectedWidget()
        if next_widget is not None:
            next_widget.selected = True
    
    def selectNext(self):
        self.selectWidget(self._select_index + 1)
    
    def selectPrevious(self):
        self.selectWidget(self._select_index - 1)
    
    def inputKey(self, key: str) -> bool:
        match key:
            case Keys.UP:
                self.selectPrevious()
                
            case Keys.DOWN:
                self.selectNext()
                
            case _:
                widget = self.getSelectedWidget()
                if widget is not None:
                    return widget.inputKey(key)
                
                return False
        return True
    
    @property
    def open_event(self) -> Event:
        return self._open_event
    @property
    def close_event(self) -> Event:
        return self._close_event
    
    def setFrame(self, value: bool):
        self._frame = value
        self.setFlagRefresh()
    @property
    def frame(self) -> bool:
        return self._frame
    @frame.setter
    def frame(self, value: bool):
        self.setFrame(value)
    
    @property
    def frame_pixel(self) -> Union[Pixel, None]:
        return self._frame_pixel
    @frame_pixel.setter
    def frame_pixel(self, value):
        self._frame_pixel = value
        self.setFlagRefresh()
        self.change_frame_pixel_event.invoke()

    @property
    def change_frame_pixel_event(self) -> Event:
        return self._change_frame_pixel_event
