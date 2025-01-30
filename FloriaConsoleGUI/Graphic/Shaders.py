from typing import Union, Iterable
from math import cos, sin, floor
from time import perf_counter

from .Pixel import *

t1 = perf_counter()

def invert(
    x: int, 
    y: int, 
    width: int, 
    height: int,
    item: Union[Pixel, None]
):
    if item is not None:
        item = item.change(
            front_color=Vec3(*map(lambda x: 255 - x, item.front_color)) if item.front_color is not None else None,
            back_color=Vec3(*map(lambda x: 255 - x, item.back_color)) if item.back_color is not None else None
        )
        
    return item

def rainbow(
    x: int, 
    y: int, 
    width: int, 
    height: int,
    item: Union[Pixel, None]
):
    if item is not None and item.back_color is None:
        indent = (t1 - perf_counter()) * 5
        
        x += indent
        y += indent
        
        color = Vec3(
            floor((cos(x*0.4)+1)*127),
            floor((sin(y*0.4)+1)*127),
            floor((cos((x+y)/2*0.4)+1)*127)
        )
        
        item = item.change(
            back_color=Vec3(*map(lambda x: 255 - x, color))
        )
        
    return item