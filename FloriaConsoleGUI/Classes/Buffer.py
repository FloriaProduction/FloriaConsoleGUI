from typing import Union, Callable, Generic, TypeVar, Iterable
import math

from .Anchor import Anchor
from .Vec import Vec2, Vec4


_T = TypeVar('_T')

class Buffer(Generic[_T]):
    empty = None
    
    def __init__(self, width: int, height: int, defualt_value: _T = None, data: Union[Iterable[_T], None] = None):
        if width < 0 or height < 0:
            raise ValueError(f'Width or height cannot be less than 0')
        
        self._size = Vec2(width, height, no_modify=True)
        
        self._defualt_value = defualt_value
        
        if data is not None:
            if len(data) != width*height:
                raise ValueError(f'The parameters for width({width}) and height({height}) do not match the len of data({len(data)})')
            self._data: list[_T] = list(data)  
        else:
            self.fill()

    @staticmethod
    def pasteFunction(
        x_parent: int, 
        y_parent: int, 
        width_parent: int, 
        height_parent: int, 
        x_child: int, 
        y_child: int, 
        width_child: int, 
        height_child: int, 
        old: Union[any, None], 
        new: Union[any, None]
    ) -> Union[any, None]:
        return new if new is not None else old
    
    def pasteArray(
        self, 
        offset_x: int, 
        offset_y: int, 
        array_width: int, 
        array_height: int, 
        array: Iterable, 
        padding: Vec4 = Vec4(0, 0, 0, 0), 
        func: Callable[[int, int, int, int, int, int, int, int, _T, _T], _T]=None
    ):
        if array is None or array_width == 0 or array_height == 0:
            return
        
        for y in range(
            max(
                -offset_y, 
                0
            ), 
            min(
                array_height - (padding.vertical + array_height + offset_y - self.height),
                array_height
            )):
            for x in range(
                max(
                    -offset_x, 
                    0
                ), 
                min(
                    array_width - (padding.horizontal + array_width + offset_x - self.width),
                    array_width
                )):
                xpos = x + offset_x + padding.left
                ypos = y + offset_y + padding.top
                
                self._data[
                    ypos * self._size.width + xpos
                ] = (func if func is not None else self.pasteFunction)(
                    xpos, ypos,
                    self.width, self.height,
                    x, y,
                    array_width, array_height,
                    self._data[
                        ypos * self._size.width + xpos
                    ],
                    array[
                        y * array_width + x
                    ]
                )
        
        # for y in range(array_height):
        #     for x in range(array_width):
        #         xpos, ypos = x + offset_x + padding.left, y + offset_y + padding.top
                
        #         if xpos >= self.width - padding.right or xpos < 0 + padding.left or\
        #             ypos >= self.height - padding.bottom or ypos < 0 + padding.top:
        #             continue
                
        #         self._data[
        #             ypos * self._size.width + xpos
        #         ] = func(
        #             self._data[
        #                 ypos * self._size.width + xpos
        #             ],
        #             array[
        #                 y * array_width + x
        #             ]
        #         )
    
    def paste(
        self, 
        offset_x: int, 
        offset_y: int, 
        buffer: Union['Buffer', None], 
        padding: Vec4 = Vec4(0, 0, 0, 0), 
        func: Callable[[int, int, int, int, int, int, int, int, _T, _T], _T]=None
    ):
        if buffer is None:
            return
        
        self.pasteArray(
            offset_x, offset_y,
            buffer.width, buffer.height, buffer.data,
            padding,
            func
        )

    def pasteByAnchor(
        self, 
        offset_x: int, 
        offset_y: int, 
        buffer: Union['Buffer', None], 
        anchor: Anchor = Anchor.left_top, 
        padding: Vec4 = Vec4(0, 0, 0, 0), 
        func: Callable[[int, int, int, int, int, int, int, int, _T, _T], _T]=None
    ):
        offset_x_calc = math.floor((self.width - padding.left - padding.right) / 2 - buffer.width/2)
        match anchor:
            case Anchor.left | Anchor.left_top | Anchor.left_bottom:
                offset_x_calc = 0
            case Anchor.right | Anchor.right_top | Anchor.right_bottom:
                offset_x_calc = self.width - buffer.width - padding.left - padding.right
                
        offset_y_calc = math.floor((self.height - padding.top - padding.bottom) / 2 - buffer.height/2)
        match anchor:
            case Anchor.top | Anchor.left_top | Anchor.right_top:
                offset_y_calc = 0
            case Anchor.bottom | Anchor.left_bottom | Anchor.right_bottom:
                offset_y_calc = self.height - buffer.height - padding.top - padding.bottom
        
        self.paste(
            offset_x_calc + offset_x, 
            offset_y_calc + offset_y, 
            buffer,
            padding,
            func
        )
    
    def fill(self, value: _T = None):
        '''
            Fill default_value if value is None
        '''
        self._data = [value if value is not None else self._defualt_value] * (self.width * self.height)
    
    def set(self, x: int, y: int, value: _T):
        self._data[y * self.width + x] = value
    def get(self, x: int, y: int) -> _T:
        return self._data[y * self.width + x]
    
    @staticmethod
    def convertFunction(
        x: int, 
        y: int, 
        width: int, 
        height: int,
        item: Union[any, None],
    ):
        return item
    
    def convert(self, func: Callable[[int, int, int, int, _T], _T]) -> 'Buffer':
        '''
            Create and convert a buffer\n
            `Don't modify` this buffer, just `create a new one`
        '''
        
        return Buffer(*self.size, self._defualt_value, 
        [
            [
                func(x, y, self.width, self.height, self.get(x, y)) 
                for x in range(self.width)
            ] 
            for y in range(self.height)
        ])      
    
    def resize(self, width: int, height: int) -> 'Buffer':
        '''
            Create a resized copy
        '''
        if self.size == (width, height):
            return self.copy()
        
        buffer = Buffer(width, height, self._defualt_value)
        
        for y in range(buffer.height):
            for x in range(buffer.width):
                buffer[x, y] = self[
                    min(max(math.floor(x * (self.width / width)), 0), self.width-1), 
                    min(max(math.floor(y * (self.height / height)), 0), self.height-1)
                ]
        
        return buffer
    
    @property
    def size(self) -> Vec2[int]:
        return self._size
    @property
    def width(self) -> int:
        return self.size.width
    @property
    def height(self) -> int:
        return self.size.height
    @property
    def data(self) -> tuple[_T]:
        return tuple(self._data)
    
    def __len__(self) -> int:
        return len(self._data)
    
    def __iter__(self):
        yield from self._data
                 
    def __getitem__(self, pos: tuple[int, int]) -> _T:
        return self.get(*pos)
    def __setitem__(self, pos: tuple[int, int], value: _T):
        self.set(*pos, value)

    @staticmethod
    def _raise_resize():
        raise RuntimeError('Size cannot be changed')
    
    def copy(self) -> 'Buffer':
        return Buffer(
            *self.size, self._defualt_value, self._data
        )
    
Buffer.empty = Buffer(0, 0, None)