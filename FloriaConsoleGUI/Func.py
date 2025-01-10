from typing import Union, Callable
from datetime import datetime, date
import json

from .Classes import Anchor

def setTextAnchor(text: str, anchor: Anchor, width: Union[int, None] = None, fillchar: chr = ' '):
    target_width = width if width is not None else len(text)
    match anchor:
        case Anchor.center:
            return text.center(target_width, fillchar)
        case Anchor.right:
            return text.rjust(target_width, fillchar)
        case _:
            return text.ljust(target_width, fillchar)

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