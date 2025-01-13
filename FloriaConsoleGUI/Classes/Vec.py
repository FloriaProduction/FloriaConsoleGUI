from typing import Union, Callable, Generic, TypeVar, Iterable
from .Event import Event

_T2 = TypeVar('_T2')
class Vec2(Generic[_T2]):
    def __init__(self, x: _T2, y: _T2):
        self._x = x
        self._y = y
        
        self._prop_for_iter: tuple[str] = ['_x', '_y']
    
        self._update_event: Event = Event()
    
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
    def y(self) -> _T2:
        return self._y
    @y.setter
    def y(self, value: _T2):
        self._setValue('_y', value)
    
    @property
    def change_event(self) -> Event:
        return self._update_event
        
    def __len__(self) -> int:
        return len(self._prop_for_iter)
        
    # def __getitem__(self, index: int) -> _T2:
    #     return self.__getattribute__(self._prop_for_iter[index])
    
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
    def __init__(self, x: _T3, y: _T3, z: _T3):
        super().__init__(x, y)
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
    def __init__(self, x: _T4, y: _T4, z: _T4, w: _T4):
        super().__init__(x, y, z)
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