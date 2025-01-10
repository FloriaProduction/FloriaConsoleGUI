from typing import Union, Iterable, Callable

from .Classes import Vec2, Vec3, Anchor, Orientation
from .Graphic import Pixel, Pixels, Widget


def toVec2(data: Union[Vec2, Iterable], default: Vec2 = Vec2(0, 0), allow_none: bool = False) -> Vec2:
    if data is None:
        return default
    if allow_none is False and None in data:
        raise ValueError()
    return data if isinstance(data, Vec2) else Vec2(*data)

def toVec3(data: Union[Vec3, Iterable], default: Vec3 = Vec3(0, 0, 0), allow_none: bool = False) -> Vec3:
    if data is None:
        return default
    if allow_none is False and None in data:
        raise ValueError()
    return data if isinstance(data, Vec3) else Vec3(*data)

def toPixel(data: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str, None], default: Pixel = None) -> Pixel:
    '''
        `data` can be of any `Iterable-Type`
    '''
    if data is None:
        return default
    elif isinstance(data, str):
        return Pixels.__dict__[data]
    elif isinstance(data, Pixel | Iterable):
        return data if isinstance(data, Pixel) else Pixel(*data)

    raise ValueError(f'data({data}) is not Pixel | tuple')
         


def toListWidgets(data: Union[Iterable[Widget], Widget]) -> list[Widget]:
    if isinstance(data, type(Widget)):
        return [data]
    if not isinstance(data, Iterable):
        raise ValueError()
    return [*data]

def toAnchor(anchor: Union[Anchor, str]) -> Anchor:
    if isinstance(anchor, Anchor):
        return anchor
    elif isinstance(anchor, str):
        return Anchor[anchor]
    raise ValueError()

def toOrientation(orientation: Union[Orientation, str]) -> Orientation:
    if isinstance(orientation, Orientation):
        return orientation
    elif isinstance(orientation, str):
        return Orientation[orientation]
    raise ValueError()
