from typing import Union, Iterable, TypeVar

from .Classes import Vec2, Vec3, Vec4, Anchor, Orientation
from .Graphic.Pixel import Pixel, Pixels
from .Graphic.Animation import Animation
from .Config import Config

def _toVecX(vec_type: type[any], data: Union[any, Iterable], default: any, allow_none: bool = False) -> any:
    if data is None:
        return default
    if not isinstance(data, Iterable) or allow_none is False and None in data:
        raise ValueError()
    return data if isinstance(data, vec_type) else vec_type(*data)

def toVec2(data: Union[Vec2, Iterable], default: Vec2 = Vec2(0, 0), allow_none: bool = False) -> Vec2:
    return _toVecX(Vec2, data, default, allow_none)
def toVec3(data: Union[Vec3, Iterable], default: Vec3 = Vec3(0, 0, 0), allow_none: bool = False) -> Vec3:
    return _toVecX(Vec3, data, default, allow_none)
def toVec4(data: Union[Vec4, Iterable], default: Vec4 = Vec4(0, 0, 0, 0), allow_none: bool = False) -> Vec4:
    return _toVecX(Vec4, data, default, allow_none)

def toPixel(data: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str, None], default: Pixel = None) -> Union[Pixel, None]:
    '''
        `data` can be of any `Iterable-Type`
    '''
    if data is None:
        return default
    elif isinstance(data, str):
        return Pixels.__dict__[data]
    elif isinstance(data, Pixel | Iterable):
        return data if isinstance(data, Pixel) else Pixel(*data)

    raise ValueError(f'data({data}) is not Pixel | Iterable')

TOLISTOBJECTS_T1 = TypeVar('TOLISTOBJECTS_T1')
def toListObjects(data: Union[Iterable[TOLISTOBJECTS_T1], TOLISTOBJECTS_T1, None]) -> list[TOLISTOBJECTS_T1]:
    if data is None:
        return []
    elif isinstance(data, Iterable):
        return [*data]
    return [data]

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

def toText(text: str) -> str:
    return text.replace('\n', '\\n').replace('\t', ' ' * Config.TAB_LENGTH)
def toMultilineText(text: str) -> str:
    return text.replace('\t', ' ' * Config.TAB_LENGTH)