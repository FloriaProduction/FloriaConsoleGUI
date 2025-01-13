from typing import Union, Iterable

from ..Classes import Vec2, Vec3, Vec4, Event, Buffer
from .Pixel import Pixel, Pixels
from .. import Converter


class BaseGraphicObject:
    def __init__(
        self,
        size: Union[Vec2[int], Iterable[int]] = None,
        offset_pos: Union[Vec3[int], Iterable[int]] = None, 
        clear_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str] = None,
        name: Union[str, None] = None,
        *args, **kwargs
        ):
        
        ''' events '''
        self.__resize_event = Event(
            self.setFlagRefresh
        )
        self.__change_clear_pixel_event = Event(
            self.setFlagRefresh
        )
        self.__set_refresh_event = Event()
        
        ''' size and pos '''
        self._offset_pos = Converter.toVec3(offset_pos)
        self._size = Converter.toVec2(size)
        self._padding: Vec4[int] = Vec4(0, 0, 0, 0)
        
        ''' buffers '''
        self._buffer: Buffer[Pixel] = Buffer.empty
        
        ''' pixels '''
        self._clear_pixel = Converter.toPixel(clear_pixel)
        
        ''' flags '''
        self._flag_refresh = True
        
        ''' other '''
        self._name = name


    def refresh(self):
        self._buffer = Buffer(
            self.size.x + sum(self.padding[2, 3]),
            self.size.y + sum(self.padding[0, 1]),
            self.clear_pixel
        )
        
        self._flag_refresh = False
    
    def render(self) -> Buffer[Pixel]:
        if self._flag_refresh:
            self.refresh()
        return self._buffer
    
    def setFlagRefresh(self):
        self._flag_refresh = True
        self.set_refresh_event.invoke()
    
    
    def setOffsetPos(self, value: Vec3[int]):
        self._offset_pos = value
    @property
    def offset_pos(self) -> Vec3[int]:
        return self._offset_pos
    @offset_pos.setter
    def offset_pos(self, value: Vec3[int]):
        self.setOffsetPos(value)
    @property
    def offset_x(self) -> int:
        return self.offset_pos.x
    @offset_x.setter
    def offset_x(self, value: int):
        self.offset_pos.x = value
    @property
    def offset_y(self) -> int:
        return self.offset_pos.y
    @offset_y.setter
    def offset_y(self, value: int):
        self.offset_pos.y = value
    @property
    def offset_z(self) -> int:
        return self.offset_pos.z
    @offset_z.setter
    def offset_z(self, value: int):
        self.offset_pos.z = value
    
    def setSize(self, value: Vec2[int]):
        self._size = value
        self.resize_event.invoke()
        value.change_event.add(
            self.resize_event.invoke
        )
    @property
    def size(self) -> Vec2[int]:
        return self._size
    @size.setter
    def size(self, value: Vec2[int]):
        self.setSize(value)
    @property
    def width(self) -> int:
        return self.size.x
    @width.setter
    def width(self, value: int):
        self.size.x = value
    @property
    def height(self) -> int:
        return self.size.y
    @height.setter
    def height(self, value: int):
        self.size.y = value
    
    @property
    def name(self) -> Union[str, None]:
        return self._name
    
    @property
    def clear_pixel(self) -> Union[Pixel, None]:
        return self._clear_pixel
    @clear_pixel.setter
    def clear_pixel(self, value: Union[Pixel, None]):
        self._clear_pixel = value
        self.change_clear_pixel_event.invoke()
    
    @property
    def resize_event(self) -> Event:
        return self.__resize_event
    @property
    def change_clear_pixel_event(self) -> Event:
        return self.__change_clear_pixel_event
    @property
    def set_refresh_event(self) -> Event:
        return self.__set_refresh_event
    
    def setPadding(self, value: Vec4[int]):
        self._padding = value
        self.__resize_event.invoke()
        value.change_event.add(
            self.__resize_event.invoke
        )
    def getPadding(self) -> Vec4[int]:
        return self._padding
    @property
    def padding(self) -> Vec4[int]:
        '''
            `up`: 0 | x\n
            `down` 1 | y\n
            `left` 2 | z\n
            `right` 3 | w
        '''
        return self.getPadding()
    @padding.setter
    def padding(self, value: Vec4[int]):
        self.setPadding(value)


class BaseGraphicContainerObject(BaseGraphicObject):
    def __init__(
        self, 
        size: Union[Vec2[int], Iterable[int]] = None,
        auto_size: bool = False,
        offset_pos: Union[Vec3[int], Iterable[int]] = None, 
        clear_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str] = None,
        name: Union[str, None] = None,
        objects: Union[Iterable[BaseGraphicObject], BaseGraphicObject] = [], 
        *args, **kwargs
    ):
        super().__init__(
            size=size, 
            offset_pos=offset_pos, 
            clear_pixel=clear_pixel, 
            name=name, 
            *args, **kwargs
        )
        
        ''' size and pos '''
        self._auto_size = auto_size
        
        ''' events '''
        self.__add_object_event = Event(
            self.setFlagRefresh
        )
        
        ''' objects '''
        self._objects: list['BaseGraphicObject'] = []
        for object in Converter.toListObjects(objects):
            self.addObject(object)
        
        ''' buffers '''
        self._objects_buffer: Buffer[Pixel] = Buffer.empty
    
    def refresh(self):
        objects = [
            (
                object.offset_x + self.padding[2],
                object.offset_y + self.padding[0],
                object.render()
            )
            for object in self._objects
        ]
        
        super().refresh()
        
        for object_data in objects:
            self._buffer.paste(*object_data)
    
        
    def addObject(self, object: BaseGraphicObject):
        self._objects.append(
            object
        )
        object.set_refresh_event.add(self.setFlagRefresh)
        self.add_object_event.invoke()
       
    
    @property
    def add_object_event(self) -> Event:
        return self.__add_object_event
    
    def __iter__(self):
        yield from self._objects
    
    def __str__(self, **kwargs):
        kwargs.update({
            "name": self._name,
            "size": self._size,
            "offset_pos": self._offset_pos
        })
        return f'{self.__class__.__name__}({' '.join([f'{key}:{value}' for key, value in kwargs.items()])})'
