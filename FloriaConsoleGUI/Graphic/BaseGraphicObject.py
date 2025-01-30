from typing import Union, Iterable, overload, Callable
from math import floor

from ..Classes import *
from .Pixel import Pixel
from .. import Converter
from .Shaders.BasePixelShader import BasePixelShader


class BaseGraphicObject:
    @overload
    def __init__(
        self,
        size: Iterable[int] = None,
        min_size: Union[Iterable[Union[int, None]], None] = None,
        max_size: Union[Iterable[Union[int, None]], None] = None,
        size_hint: Union[Iterable[Union[float, None]], None] = None,
        padding: Union[Iterable[int]] = None,
        offset_pos: Union[Iterable[int]] = None, 
        pos_hint: dict[str, Union[int, None]] = {},
        clear_pixel: Union[Pixel, tuple[Iterable[int], Iterable[int], str], str] = None,
        name: Union[str, None] = None,
        shader: Union[BasePixelShader, None] = None,
        **kwargs
    ): ...
    
    def __init__(self, **kwargs):
        
        # events 
        self.__resize_event = Event()
        self.__move_event = Event()
        self.__change_clear_pixel_event = Event(
            self.setFlagRefresh
        )
        self.__set_refresh_event = Event()
        
        # size and pos
        self._size = Converter.toVec2(kwargs.get('size'))
        self._padding: Vec4[int] = Converter.toVec4(kwargs.get('padding'))
        self._min_size = Converter.toVec2(kwargs.get('min_size'), Vec2(None, None), True)
        self._max_size = Converter.toVec2(kwargs.get('max_size'), Vec2(None, None), True)
        self._size_hint = Converter.toVec2(kwargs.get('size_hint'), Vec2(None, None), True)
        self._offset_pos = Converter.toVec3(kwargs.get('offset_pos'))
        pos_hint: dict[str, Union[int, None]] = kwargs.get('pos_hint', {})
        self._pos_hint = Vec4(
            pos_hint.get('top', None),
            pos_hint.get('bottom', None),
            pos_hint.get('left', None),
            pos_hint.get('right', None)
        )
        
        # buffers
        self._buffer: Buffer[Pixel] = None
        
        # pixels
        self._clear_pixel = Converter.toPixel(kwargs.get('clear_pixel'))
        
        # shaders
        self._shader: Union[BasePixelShader, None] = kwargs.get('shader')
        
        # flags
        self._flag_refresh = True
        
        # other
        self._name = kwargs.get('name')
    
    async def refresh(self):
        self._buffer = Buffer(
            self.width + self.padding.horizontal,
            self.height + self.padding.vertical,
            self.clear_pixel
        )
        
        self._flag_refresh = False
        
    async def render(self) -> Buffer[Pixel]:
        if self._flag_refresh:
            await self.refresh()
        return self._buffer if self._shader is None else self._buffer.convert(self._shader.convertFunction)
    
    async def awaitingRefresh(self):
        return False
    
    def setFlagRefresh(self):
        self._flag_refresh = True
        self.set_refresh_event.invoke()
    
    @property
    def offset_pos(self) -> Vec3[int]:
        return self._offset_pos
    @offset_pos.setter
    def offset_pos(self, value: Vec3[int]):
        self._offset_pos = value
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
    @property
    def pos_hint(self) -> Vec4[Union[int, None]]:
        return self._pos_hint
    @pos_hint.setter
    def pos_hint(self, value: Vec4[Union[int, None]]):
        self._pos_hint = value

    def setSize(self, value: Iterable[int]):
        self._size = Vec2(*value)
        self._size.change_event.add(
            self.resize_event.invoke,
            self.setFlagRefresh
        )
        self.resize_event.invoke()
        self.setFlagRefresh()
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
    def size(self, value: Iterable[int]):
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
    
    def getMinSize(self) -> Vec2[Union[int, None]]:
        return self._min_size
    @property
    def min_size(self) -> Vec2[Union[int, None]]:
        return self.getMinSize()
    @min_size.setter
    def min_size(self, value: Iterable[Union[int, None]]):
        self._min_size = Vec2(*value)
        self.setFlagRefresh()
    
    def getMaxSize(self) -> Vec2[Union[int, None]]:
        return self._max_size
    @property
    def max_size(self) -> Vec2[Union[int, None]]:
        return self.getMaxSize()
    @max_size.setter
    def max_size(self, value: Iterable[Union[int, None]]):
        self._max_size = Vec2(*value)
        self.setFlagRefresh()
    
    def getSizeHint(self) -> Vec2[Union[float, None]]:
        return self._size_hint
    @property
    def size_hint(self) -> Vec2[Union[float, None]]:
        return self.getSizeHint()
    @size_hint.setter
    def size_hint(self, value: Vec2[Union[float, None]]):
        self._size_hint = value
        self.setFlagRefresh()

    @property
    def name(self) -> Union[str, None]:
        return self._name
    
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
    @property
    def move_event(self) -> Event:
        return self.__move_event
    

class BaseGraphicContainerObject(BaseGraphicObject):
    @overload
    def __init__(
        self,
        size: Iterable[int] = None,
        min_size: Union[Iterable[Union[int, None]], None] = None,
        max_size: Union[Iterable[Union[int, None]], None] = None,
        size_hint: Union[Iterable[Union[float, None]], None] = None,
        padding: Union[Iterable[int]] = None,
        offset_pos: Union[Iterable[int]] = None, 
        pos_hint: Union[Iterable[Union[int, None]], None] = None,
        clear_pixel: Union[Pixel, tuple[Iterable[int], Iterable[int], str], str] = None,
        name: Union[str, None] = None,
        objects: Union[Iterable[BaseGraphicObject], BaseGraphicObject] = [], 
        size_by_objects: bool = True,
        objects_direction: Union[Orientation, None] = None,
        gap: int = 0,
        scroll: Iterable[int] = None,
        **kwargs
    ):
        """
        Args:
            objects (`Iterable[BaseGraphicObject]`, `BaseGraphicObject`): Дочерние объекты. Defaults to [].
            size_by_objects (`bool`, `optional`): Подгонять размер по дочерним объектам. Defaults to True.
            objects_direction (`Orientation`, `None`): Направление объектов, None если не нужно. Defaults to None.
            gap (`int`): Расстояние между объектами. Defaults to 0.
            scroll (`Iterable[int]`): прокручивание объектов внутри. Defaults [0, 0]
        """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # events 
        self.__add_object_event = EventKwargs()
        self.__remove_object_event = EventKwargs()
        self.__remove_all_objects_event = Event()
        
        # objects 
        self._objects: list['BaseGraphicObject'] = []
        for object in Converter.toListObjects(kwargs.get('objects', [])):
            self.addObject(object)
        self._gap: int = kwargs.get('gap', 0)
        self._size_by_objects: bool = kwargs.get('size_by_objects', True)
        orientation = kwargs.get('objects_direction', None)
        self._objects_direction: Union[Orientation, None] = Converter.toOrientation(orientation) if orientation is not None else None
        self._scroll: Vec2[int] = Converter.toVec2(kwargs.get('scroll'))
    
    
    async def refresh(self):
        for object in self._objects:
            # size_hint
            if object.size_hint.width is not None:
                object.width = floor(
                    (self.min_size.width if self.min_size.width is not None else self.width) if self.size_by_objects else self.width
                    * object.size_hint.width - object.padding.horizontal
                )
            if object.size_hint.height is not None:
                object.height = floor(
                    (self.min_size.height if self.min_size.height is not None else self.height) if self.size_by_objects else self.height
                    * object.size_hint.height - object.padding.vertical
                )
        
            # pos_hint
            if object.pos_hint.top is not None:
                object.offset_y = floor(self.height * object.pos_hint.top)
            
            elif object.pos_hint.bottom is not None:
                object.offset_y = floor(self.height - (object.height - self.height * object.pos_hint.top))

            if object.pos_hint.left is not None:
                object.offset_x = floor(self.width * object.pos_hint.left)
            
            elif object.pos_hint.right is not None:
                object.offset_x = floor(self.width - (object.width - self.width * object.pos_hint.right))
        
        if self.objects_direction is not None:
            indent_x = indent_y = 0
            for object in self._objects:
                object.offset_x = indent_x
                object.offset_y = indent_y
                
                match self.objects_direction:
                    case Orientation.vertical:
                        indent_y += object.height + object.padding.vertical + self.gap
                    case Orientation.horizontal:
                        indent_x += object.width + object.padding.horizontal + self.gap
                    case _:
                        raise RuntimeError()
    
        width = height = 0
        for object in self._objects:
            width, height = max(width, object.offset_x + object.width + object.padding.horizontal), \
                            max(height, object.offset_y + object.height + object.padding.vertical)
        
        objects_buffer = Buffer(
            width, 
            height
        )
        
        for object in self._objects:
            objects_buffer.paste(
                object.offset_x, 
                object.offset_y, 
                await object.render()
            )
            
        if self.size_by_objects:
            self.size = Vec2(
                *objects_buffer.size
            )
        
        await super().refresh()
        
        self._buffer.paste(
            -self.scroll.x,
            -self.scroll.y,
            objects_buffer,
            self.padding
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
        object.move_event.add(self.setFlagRefresh)
        self.add_object_event.invoke(object=object)
        self.setFlagRefresh()
    
    def removeObject(self, object: BaseGraphicObject):
        self._objects.remove(
            object
        )
        self.remove_object_event.invoke(object=object)
        self.setFlagRefresh()
    
    def removeAllObjects(self):
        self._objects.clear()
        self.remove_all_objects_event.invoke()
        self.setFlagRefresh()
    
    async def awaitingRefresh(self):
        for object in self._objects:
            if await object.awaitingRefresh():
                return True
        return False

    @property
    def add_object_event(self) -> EventKwargs:
        '''
            func(object: BaseGraphicObject) -> None
        '''
        return self.__add_object_event
    @property
    def remove_object_event(self) -> EventKwargs:
        '''
            func(object: BaseGraphicObject) -> None
        '''
        return self.__remove_object_event
    @property
    def remove_all_objects_event(self) -> Event:
        return self.__remove_all_objects_event
    
    
    @property
    def gap(self) -> int:
        return self._gap
    @gap.setter
    def gap(self, value: int):
        self._gap = value
        self.setFlagRefresh()
    
    @property
    def objects_direction(self) -> Orientation:
        return self._objects_direction
    @objects_direction.setter
    def objects_direction(self, value: Orientation):
        self._objects_direction = value
        self.setFlagRefresh()
    
    @property
    def size_by_objects(self) -> bool:
        return self._size_by_objects
    
    @property
    def scroll(self) -> Vec2[int]:
        return self._scroll
    @scroll.setter
    def scroll(self, value: Vec2[int]):
        self._scroll = value
        self._scroll.change_event.add(
            self.setFlagRefresh
        )
        self.setFlagRefresh()
    
    def __iter__(self):
        yield from self._objects
    
    def __str__(self, **kwargs):
        kwargs.update({
            "name": self._name,
            "size": self._size,
            "offset_pos": self._offset_pos
        })
        return f'{self.__class__.__name__}({' '.join([f'{key}:{value}' for key, value in kwargs.items()])})'
