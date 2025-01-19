from typing import Union, Iterable

from ..Classes import Vec2, Vec3, Vec4, Event, Buffer, Orientation
from .Pixel import Pixel
from .. import Converter


class BaseGraphicObject:
    def __init__(
        self,
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
        
        # events 
        self.__resize_event = Event(
            self.setFlagRefresh
        )
        self.__change_clear_pixel_event = Event(
            self.setFlagRefresh
        )
        self.__set_refresh_event = Event()
        
        # size and pos
        self._offset_pos = Converter.toVec3(offset_pos)
        self._size = Converter.toVec2(size)
        self._padding: Vec4[int] = Converter.toVec4(padding)
        self._min_size = Converter.toVec2(min_size, Vec2(None, None), True)
        self._max_size = Converter.toVec2(max_size, Vec2(None, None), True)
        self._can_be_moved = can_be_moved
        
        # buffers
        self._buffer: Buffer[Pixel] = None
        
        # pixels
        self._clear_pixel = Converter.toPixel(clear_pixel)
        
        # flags
        self._flag_refresh = True
        
        # other
        self._name = name
    
    async def refresh(self):
        self._buffer = Buffer(
            self.width + self.padding.horizontal,
            self.height + self.padding.vertical,
            self.clear_pixel
        )
        
        self._flag_refresh = False
    
    async def awaitingRefresh(self) -> bool:
        return False
    
    async def render(self) -> Buffer[Pixel]:
        if self._flag_refresh:
            await self.refresh()
        return self._buffer
    
    def setFlagRefresh(self):
        self._flag_refresh = True
        self.set_refresh_event.invoke()
    
    def setOffsetPos(self, value: Vec3[int]):
        self._offset_pos = value
    def getOffsetPos(self) -> Vec3[int]:
        return self._offset_pos
    @property
    def offset_pos(self) -> Vec3[int]:
        return self.getOffsetPos()
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
    def getSize(self) -> Vec2[int]:
        return Vec2(
            max(
                max(
                    self._size.width,  
                    self._min_size.width if self._min_size.width is not None else 0
                ), 
                min(
                    self._size.width,
                    self._max_size.width if self._max_size.width is not None else self._size.width
                )
            ),
            max(
                max(
                    self._size.height, 
                    self._min_size.height if self._min_size.height is not None else 0
                ), 
                min(
                    self._size.height,
                    self._max_size.height if self._max_size.height is not None else self._size.height
                )
            )
        )
    @property
    def size(self) -> Vec2[int]:
        return self.getSize()
    @size.setter
    def size(self, value: Vec2[int]):
        self.setSize(value)
    @property
    def width(self) -> int:
        return self.size.width
    @width.setter
    def width(self, value: int):
        self._size.width = value
    @property
    def height(self) -> int:
        return self.size.height
    @height.setter
    def height(self, value: int):
        self._size.height = value
        
    @property
    def min_size(self) -> Vec2[int]:
        return self._min_size
    @size.setter
    def min_size(self, value: Vec2[int]):
        self._min_size = value
        self.setFlagRefresh()
        
    @property
    def max_size(self) -> Vec2[int]:
        return self._max_size
    @size.setter
    def max_size(self, value: Vec2[int]):
        self._max_size = value
        self.setFlagRefresh()
    
    @property
    def name(self) -> Union[str, None]:
        return self._name
    
    def getClearPixel(self) -> Union[Pixel, None]:
        return self._clear_pixel
    
    def setClearPixel(self, value: Union[Pixel, None]):
        self._clear_pixel = value
        self.change_clear_pixel_event.invoke()
    
    @property
    def clear_pixel(self) -> Union[Pixel, None]:
        return self.getClearPixel()
    @clear_pixel.setter
    def clear_pixel(self, value: Union[Pixel, None]):
        self.setClearPixel(value)
    
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
            `bottom` 1 | y\n
            `left` 2 | z\n
            `right` 3 | w
        '''
        return self.getPadding()
    @padding.setter
    def padding(self, value: Vec4[int]):
        self.setPadding(value)
        
    @property
    def can_be_moved(self) -> bool:
        return self._can_be_moved
    @can_be_moved.setter
    def can_be_moved(self, value: bool):
        self._can_be_moved = value


class BaseGraphicContainerObject(BaseGraphicObject):
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
        objects: Union[Iterable[BaseGraphicObject], BaseGraphicObject] = [], 
        direction: Union[Orientation, None] = Orientation.horizontal,
        gap: int = 0,
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
        self._direction: Orientation = Converter.toOrientation(direction) if direction is not None else None
        self._gap: int = gap
        
        ''' buffers '''
        self._objects_buffer: Buffer[Pixel] = Buffer.empty
    
    async def refresh(self):
        objects = [
            (
                object.offset_x,
                object.offset_y,
                await object.render(),
                object.can_be_moved
            )
            for object in self._objects
        ]
        
        if self._direction is None:
            await super().refresh()
            
            self._objects_buffer = Buffer(
                max(self.width - self.padding.horizontal, 0),
                max(self.height - self.padding.vertical, 0),
                self.clear_pixel
            )
            
            for object_data in objects:
                self._objects_buffer.paste(*object_data[:3])
                
            
        else:
            object_buffer_width = object_buffer_height = 0
            
            for object in self._objects:
                if object.can_be_moved is False:
                    continue
                
                match self._direction:
                    case Orientation.vertical:
                        object_buffer_width = max(object.width + object.padding.horizontal, object_buffer_width)
                    case _:
                        object_buffer_width += object.width + object.padding.horizontal + self.gap
                
                match self._direction:
                    case Orientation.horizontal:
                        object_buffer_height = max(object.height + object.padding.vertical, object_buffer_height)
                    case _:
                        object_buffer_height += object.height + object.padding.vertical + self.gap
            
            if self._direction is Orientation.horizontal:
                object_buffer_width -= 1
            else:
                object_buffer_height -= 1
            
            self._objects_buffer = Buffer(
                object_buffer_width,
                object_buffer_height,
                self.clear_pixel
            )
            
            self.size = Vec2(
                self._objects_buffer.width,
                self._objects_buffer.height
            )
            
            await super().refresh()
            
            x_indent = y_indent = 0
            for object in objects:
                if object[3] is True: # object can be moved
                    self._objects_buffer.paste(
                        x_indent, y_indent,
                        object[2]
                    )
                    
                    if self._direction is Orientation.horizontal:
                        x_indent+=object[2].width + self.gap
                    else:
                        y_indent+=object[2].height + self.gap
                else:
                    self._objects_buffer.paste(*object[:3])
                
        self._buffer.paste(
            self.padding.left, self.padding.top,
            self._objects_buffer
        )
    
    async def render(self):
        for object in self._objects:
            if await object.awaitingRefresh():
                self.setFlagRefresh()
                break
        
        return await super().render()
    
    def addObject(self, object: BaseGraphicObject):
        self._objects.append(
            object
        )
        object.set_refresh_event.add(self.setFlagRefresh)
        self.add_object_event.invoke()
    
    @property
    def add_object_event(self) -> Event:
        return self.__add_object_event
    
    @property
    def gap(self) -> int:
        return self._gap
    @gap.setter
    def gap(self, value: int):
        self._gap = value
    
    def __iter__(self):
        yield from self._objects
    
    def __str__(self, **kwargs):
        kwargs.update({
            "name": self._name,
            "size": self._size,
            "offset_pos": self._offset_pos
        })
        return f'{self.__class__.__name__}({' '.join([f'{key}:{value}' for key, value in kwargs.items()])})'
