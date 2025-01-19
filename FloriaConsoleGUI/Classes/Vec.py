from typing import Union, Callable, Generic, TypeVar, Iterable, overload
from .Event import Event


_T2 = TypeVar('_T2')
class Vec2(Generic[_T2]):
    @overload
    def __init__(self, width: _T2, height: _T2, no_modify=False): ...
    
    @overload
    def __init__(self, x: _T2, y: _T2, no_modify=False): ...
    
    def __init__(self, x: _T2, y: _T2, **kwargs):
        self._x = x
        self._y = y
        
        self._prop_for_iter: tuple[str] = ['_x', '_y']
    
        self._no_modify: bool = kwargs.get('no_modify', False)
    
        self._update_event: Event = Event()
        
        if self._no_modify:
            self._update_event.add(lambda: self.raise_exc(f'{self} cannot be modify'))
        
    @staticmethod
    def raise_exc(message: str):
        raise RuntimeError(message)
    
    def _setValue(self, attrib_name: str, value: _T2):
        self.__setattr__(attrib_name, value)
        self._update_event.invoke()
    
    @property
    def x(self) -> _T2:
        return self._x
    @x.setter
    def x(self, value: _T2):
        self._setValue('_x', value)
    @property
    def width(self) -> _T2:
        return self.x
    @width.setter
    def width(self, value: _T2):
        self.x = value
        
    @property
    def y(self) -> _T2:
        return self._y
    @y.setter
    def y(self, value: _T2):
        self._setValue('_y', value)
    @property
    def height(self) -> _T2:
        return self.y
    @height.setter
    def height(self, value: _T2):
        self.y = value
    
    @property
    def change_event(self) -> Event:
        return self._update_event
        
    def __len__(self) -> int:
        return len(self._prop_for_iter)
    
    def __getitem__(self, index: Union[int, tuple[int]]) -> Union[tuple[_T2], _T2]:
        if isinstance(index, int):
            return self.__getattribute__(self._prop_for_iter[index])
        
        return tuple([
            self.__getattribute__(self._prop_for_iter[i]) for i in index
        ])
        
    def __setitem__(self, index: int, value: _T2):
        self.__setattr__(self._prop_for_iter[index], value)
    
    def __iter__(self):
        yield from [self.__getattribute__(attrib_name) for attrib_name in self._prop_for_iter]
    

    def toTuple(self) -> tuple[_T2]:
        return tuple([self.__getattribute__(attrib_name) for attrib_name in self._prop_for_iter])

    @staticmethod
    def _calc(arr1: Iterable, arr2: Iterable, func: Callable[[any, any], any] = lambda x, y: x + y) -> tuple:
        if len(arr1) > len(arr2):
            raise ValueError()
        
        return tuple([func(arr1[i], arr2[i]) for i in range(len(arr1))])
    
    def __add__(self, other: Iterable):
        return self.__class__(*self._calc(self, other, lambda x, y: x + y))
    
    def __sub__(self, other: Iterable):
        return self.__class__(*self._calc(self, other, lambda x, y: x - y))
        
    def __mul__(self, other: Iterable):
        return self.__class__(*self._calc(self, other, lambda x, y: x * y))

    def __truediv__(self, other: Iterable):
        return self.__class__(*self._calc(self, other, lambda x, y: x / y))
    
    def __iadd__(self, other: Iterable):
        data = self + other
        for i in range(len(data)):
            self[i] = data[i]
        return self
    
    def __isub__(self, other: Iterable):
        data = self - other
        for i in range(len(data)):
            self[i] = data[i]
        return self
        
    def __imul__(self, other: Iterable):
        data = self * other
        for i in range(len(data)):
            self[i] = data[i]
        return self

    def __itruediv__(self, other: Iterable):
        data = self / other
        for i in range(len(data)):
            self[i] = data[i]
        return self

    def __eq__(self, value: Iterable):
        return self.toTuple() == value
    
    def __str__(self):
        return f'Vec2({self._x};{self._y})'


_T3 = TypeVar('_T3')
class Vec3(Vec2, Generic[_T3]):
    @overload
    def __init__(self, x: _T2, y: _T2, z: _T3, no_modify=False): ...
    
    def __init__(self, x: _T3, y: _T3, z: _T3, **kwargs):
        super().__init__(x, y, **kwargs)
        self._z = z
        
        self._prop_for_iter = (*self._prop_for_iter, '_z')
    
    def __str__(self):
        return f'Vec3({self._x};{self._y};{self._z})'
    
    @property
    def z(self) -> _T3:
        return self._z
    @z.setter
    def z(self, value: _T3):
        self._setValue('_z', value)


_T4 = TypeVar('_T4')
class Vec4(Vec3, Generic[_T4]):
    @overload
    def __init__(self, top: _T4, bottom: _T4, left: _T2, right: _T2, no_modify=False): ...
    @overload
    def __init__(self, x: _T2, y: _T2, z: _T4, w: _T4, no_modify=False): ...
    
    def __init__(self, x: _T4, y: _T4, z: _T4, w: _T4, **kwargs):
        super().__init__(x, y, z, **kwargs)
        self._w = w
        
        self._prop_for_iter = (*self._prop_for_iter, '_w')
    
    def __str__(self):
        return f'Vec4({self._x};{self._y};{self._z};{self._w})'
    
    @property
    def w(self) -> _T4:
        return self._w
    @w.setter
    def w(self, value: _T4):
        self._setValue('_w', value)
    
    @property
    def top(self) -> _T4:
        return self.x
    @top.setter
    def top(self, value: _T4):
        self.x = value
    
    @property
    def bottom(self) -> _T4:
        return self.y
    @bottom.setter
    def bottom(self, value: _T4):
        self.y = value
    
    @property
    def left(self) -> _T4:
        return self.z
    @left.setter
    def left(self, value: _T4):
        self.z = value
    
    @property
    def right(self) -> _T4:
        return self.w
    @right.setter
    def right(self, value: _T4):
        self.w = value
        
    @property
    def horizontal(self) -> _T4:
        return self.left + self.right
    
    @property
    def vertical(self) -> _T4:
        return self.top + self.bottom
    
    