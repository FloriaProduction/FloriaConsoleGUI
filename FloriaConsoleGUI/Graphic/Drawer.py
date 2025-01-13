from typing import Union

from ..Classes import Buffer, Vec3
from .Pixel import Pixel
from ..GVars import GVars

# ┘ └ │ ├ ┬
# ┐ ┌ ─ ┴ ┤ ┼
        
class FramePixel(Pixel):
    pass

class Drawer:
    _cache: dict[str, Buffer[Pixel]] = {}
    
    @classmethod
    def _putToCache(cls, key: str, value: Buffer[Pixel]):
        cls._cache[key] = value
        if len(cls._cache) > GVars.DRAWER_MAX_SIZE_CACHE:
            cls._cache.pop(tuple(cls._cache.keys())[0])
    
    @classmethod
    def _genKey(cls, **kwargs) -> str:
        return '_'.join([f'{key}:{value}' for key, value in kwargs.items()])
    
    @classmethod
    def frame(cls, width: int, height: int, front_color: Union[Vec3, None], back_color: Union[Vec3, None]) -> Buffer[Pixel]:        
        if width == 0 or height == 0:
            return Buffer.empty
        
        key = cls._genKey(func='frame', width=width, height=height, back_color=back_color, front_color=front_color)
        
        if key not in cls._cache:
            buffer: Buffer[Pixel] = Buffer(width, height, None)
            
            pixel = FramePixel(front_color, back_color)
            
            for x in range(1, width-1):
                buffer[x, 0] = buffer[x, height-1] = Pixel.changePixel(pixel, '─')
                
            for y in range(1, height-1):
                buffer[0, y] = buffer[width-1, y] = Pixel.changePixel(pixel, '│')
            
            buffer[0, 0]              = Pixel.changePixel(pixel, '┌')
            buffer[0, height-1]       = Pixel.changePixel(pixel, '└')
            buffer[width-1, 0]        = Pixel.changePixel(pixel, '┐')
            buffer[width-1, height-1] = Pixel.changePixel(pixel, '┘')
            
            cls._putToCache(key, buffer)
            
        return cls._cache[key]
    
    @classmethod
    def mergeFramePixels(cls, pixel1: Union[FramePixel, None], pixel2: Union[FramePixel, None]) -> FramePixel:       
        def inArr(*args) -> bool:
            for symbol in args:
                if symbol not in arr:
                    return False
            return True
        
        if pixel2 is None:
            return pixel1
               
        if not (isinstance(pixel1, FramePixel) and isinstance(pixel2, FramePixel)):
            return pixel2
        
        new_symbol = pixel2.symbol
        arr = (pixel1.symbol, pixel2.symbol)
        
        # ┘ └ │ ├ ┬
        # ┐ ┌ ─ ┴ ┤ ┼
        
        if arr[0] == arr[1]:
            new_symbol = pixel2.symbol
        elif inArr('─', '│') or inArr('┼') or \
            inArr('┐', '└') or inArr('┘', '┌') or \
            inArr('├', '┤') or inArr('┴', '┬') or \
            inArr('├', '┘') or inArr('├', '┐') or \
            inArr('┤', '└') or inArr('┤', '┌') or \
            inArr('┬', '┘') or inArr('┴', '┐') or \
            inArr('┬', '└') or inArr('┴', '┌'):
            new_symbol = '┼'
        elif inArr('┌', '└') or inArr('├') or \
            inArr('│', '└') or inArr('│', '┌'):
            new_symbol = '├'
        elif inArr('┐', '┘') or inArr('┤') or \
            inArr('│', '┘') or inArr('│', '┐'):
            new_symbol = '┤'
        elif inArr('┘', '└') or inArr('┴') or \
            inArr('─', '└') or inArr('─', '┘'):
            new_symbol = '┴'
        elif inArr('┌', '┐') or inArr('┬') or \
            inArr('─', '┌') or inArr('─', '┐'):
            new_symbol = '┬'
        
        return Pixel.changePixel(pixel2, symbol=new_symbol)
        
