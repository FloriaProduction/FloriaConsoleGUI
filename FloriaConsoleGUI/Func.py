from typing import Union, Callable
from datetime import datetime, date
import json

from .Classes import Anchor, Vec2, Vec3
from .Graphic.Pixel import Pixel
from .Graphic.Widgets import Widget
from .Graphic.Windows import Window

def setTextAnchor(text: str, anchor: Anchor, width: Union[int, None] = None, fillchar: chr = ' ', crop: bool = False):
    target_width = width if width is not None else len(text)
    result = '?'
    match anchor:
        case Anchor.center:
            result = text.center(target_width, fillchar)
        case Anchor.right:
            result = text.rjust(target_width, fillchar)
        case _:
            result = text.ljust(target_width, fillchar)
    if crop:
        return result[:width]
    return result

def readFile(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as file:
        return " ".join(file.readlines())

def saveFile(path: str, data: str) -> str:
    with open(path, 'w', encoding='utf-8') as file:
        file.write(data)

def custom_object_hook(data: dict[str, any]):
    for key, value in data.items():
        if isinstance(value, datetime | date):
            data[key] = value.strftime('%d.%m.%Y %H:%M:%S')
        elif isinstance(value, dict):
            data[key] = custom_object_hook(value)
        elif isinstance(value, list | tuple):
            data[key] = list([custom_object_hook(item) for item in value])
    return data

def readJson(path: str, object_pairs_hook: Callable[[tuple[str, any]], tuple[str, any]] = None) -> dict[str, any]:
    return json.loads(readFile(path), object_pairs_hook=object_pairs_hook)

def saveJson(path: str, data: dict[str, any]):
    saveFile(path, json.dumps(data, ensure_ascii=False, indent=4))


def calculateSizeByItems(data: list[Union[Window, Widget]]) -> tuple[Vec2[int], Vec2[int]]:
    width = height = 0
    for item in data:
        width = max(item.offset_x + item.width, width)
        height = max(item.offset_y + item.height, height)
    
    return Vec2(width, height)

def choisePixel(*args: Pixel, **kwargs):
    '''
        default: Pixel = Pixel.empty
    '''
    for pixel in args:
        if pixel is not None:
            return pixel
    return kwargs.get('default', Pixel.empty)