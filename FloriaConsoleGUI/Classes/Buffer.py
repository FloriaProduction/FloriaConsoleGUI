from typing import Union, Callable, Generic, TypeVar, Iterable
import math
from copy import deepcopy

from .Vec import Vec2

_T = TypeVar('_T')

class Buffer(Generic[_T]):
    empty = None
    
    def __init__(self, width: int, height: int, defualt_value: _T = None, data: Union[Iterable[_T], None] = None):
        if width < 0 or height < 0:
            raise ValueError(f'Width or height cannot be less than 0')
        
        self._size = Vec2(width, height)
        self._size.change_event.add(self._raise_resize)
        
        self._defualt_value = defualt_value
        
        if data is not None:
            if len(data) != width*height:
                raise ValueError(f'The parameters for width({width}) and height({height}) do not match the len of data({len(data)})')
            self._data: list[_T] = list(data)  
        else:
            self.fill()


    def paste(self, offset_x: int, offset_y: int, buffer: Union['Buffer', None], func: Callable[[_T, _T], _T] = lambda old, new: new if new is not None else old):
        '''
            func: function(self_value, other_value) -> new_value
        '''
        if buffer is None or buffer.size.x == 0 or buffer.size.y == 0:
            return
        
        for y in range(buffer.height):
            for x in range(buffer.width):
                pos = Vec2(
                    offset_x + x, 
                    offset_y + y
                )
                if 0 <= pos.x < self.width and 0 <= pos.y < self.height:
                    self[*pos] = func(self.get(*pos), buffer[x, y])
        

    def fill(self, value: _T = None):
        '''
            Fill default_value if value is None
        '''
        self._data = [value if value is not None else self._defualt_value] * (self.width * self.height)
    
    def set(self, x: int, y: int, value: _T):
        self._data[y * self.width + x] = value
    def get(self, x: int, y: int) -> _T:
        return self._data[y * self.width + x]
    
    def convert(self, func: Callable[[_T], any]) -> 'Buffer':
        '''
            Create and convert a buffer\n
            `Don't modify` this buffer, just `create a new one`
        '''
        
        return Buffer(*self.size, self._defualt_value, (func(item) for item in self._data))        
    
    def resize(self, width: int, height: int) -> 'Buffer':
        if self.size == (width, height):
            return self.copy()
        
        buffer = Buffer(width, height, self._defualt_value)
        
        xk = self.width / width 
        yk = self.height / height
        
        for y in range(buffer.height):
            for x in range(buffer.width):
                buffer[x, y] = self[
                    min(max(math.floor(x*xk), 0), self.width-1), 
                    min(max(math.floor(y*yk), 0), self.height-1)
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
        return deepcopy(self)
    
Buffer.empty = Buffer(0, 0, None)