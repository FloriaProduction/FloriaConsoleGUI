from typing import Union, Iterable, overload

from ..BaseGraphicObject import BaseGraphicContainerObject
from ..Pixel import *
from ..Drawer import Drawer
from ..Widgets.Widget import Widget
from ..Widgets.InteractiveWidget import InteractiveWidget
from ...Classes import Event, Vec2, Vec3, Vec4, Keys, Orientation

from ... import Converter
from ... import Func


class Window(BaseGraphicContainerObject):    
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
        frame_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str] = Pixels.white_black,
        *args, **kwargs
    ): ...
    
    def __init__(self, **kwargs):
        kwargs.update({
            'objects': kwargs.get('widgets', []),
            'size_by_objects': kwargs.get('size_by_objects', False)
        })
        super().__init__(**kwargs)
        
        ''' events '''
        self.__open_event = Event()
        self.__close_event = Event()
        self.__change_frame_pixel_event = Event()
        self.__focus_event = Event(
            self.focus
        )
        self.__blur_event = Event(
            self.blur
        )
        
        ''' pixels ''' 
        self._frame_pixel = Converter.toPixel(kwargs.get('frame_pixel'), default=Pixels.white_black)
        
        ''' interact_objects '''
        self._select_index: int = 0
        self._interact_objects: list[InteractiveWidget] = []
        self.updateInteractWidgets()
        self.add_object_event.add(self.updateInteractWidgets)
        
        ''' other '''
        self._frame = kwargs.get('frame', True)
    
    def focus(self):
        widget = self.getSelectedWidget()
        if widget:
            widget.selected = True
    
    def blur(self):
        widget = self.getSelectedWidget()
        if widget:
            widget.selected = False
            
    
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
        if previous_widget:
            previous_widget.selected = False
            
        self._select_index = index
        self._normalizeSelectIndex()
        
        next_widget = self.getSelectedWidget()
        if next_widget:
            next_widget.selected = True
    
    def selectNext(self):
        self.selectWidget(self._select_index + 1)
    
    def selectPrevious(self):
        self.selectWidget(self._select_index - 1)
    
    def inputKey(self, key: str) -> bool:
        match key:
            # case Keys.CTRL_LEFT:
            #     self.offset_x -= 1
            # case Keys.CTRL_RIGHT:
            #     self.offset_x += 1
            # case Keys.CTRL_DOWN:
            #     self.offset_y += 1
            # case Keys.CTRL_UP:
            #     self.offset_y -= 1
            
            case Keys.UP:
                self.selectPrevious()
                
            case Keys.DOWN:
                self.selectNext()
                
            case _:
                widget = self.getSelectedWidget()
                if widget is not None:
                    input_result = widget.inputKey(key)
                    widget.input_key_event.invoke(key=key)
                    return input_result
                    
                    
                return False
        return True
    
    def getClearPixel(self):
        return Func.choisePixel(super().getClearPixel(), Pixel.empty)
    
    @property
    def open_event(self) -> Event:
        return self.__open_event
    @property
    def close_event(self) -> Event:
        return self.__close_event
    
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
        return self.__change_frame_pixel_event
    
    @property
    def focus_event(self) -> Event:
        return self.__focus_event
    @property
    def blur_event(self) -> Event:
        return self.__blur_event
