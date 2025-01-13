from typing import Union, Iterable
import copy

from ..Classes import Vec3
from ..GVars import GVars

class Pixel:
    empty = None
    clearANSII = f'\033[0m'
    
    def __init__(
        self, 
        front_color: Union[Vec3[int], Iterable[int]] = None, 
        back_color: Union[Vec3[int], Iterable[int]] = None, 
        symbol: chr = None
    ):
        self.front_color = Vec3(*front_color) if isinstance(front_color, Iterable) else front_color
        self.back_color = Vec3(*back_color) if isinstance(back_color, Iterable) else back_color
        self.symbol = symbol if symbol is not None else ' '
        
        if isinstance(self.front_color, int):
            raise

    
    @staticmethod
    def fromRGB(br: int, bg: int, bb: int, symbol: chr = None) -> 'Pixel':
        return Pixel(back_color=Vec3(br, bg, bb), symbol=symbol)
    
    @staticmethod
    def changePixel(pixel: 'Pixel', symbol: chr = None, front_color: Vec3 = None, back_color: Vec3 = None) -> 'Pixel':
        '''
            create a copy of the pixel and change it
        '''
        new_pixel = pixel.copy()
        
        if symbol is not None:
            new_pixel.symbol = symbol
        
        if front_color is not None:
            new_pixel.front_color = front_color
        
        if back_color is not None:
            new_pixel.back_color = back_color    
        
        return new_pixel
    
    # WIP
    
    # @staticmethod
    # def mixStatic(col1: 'Pixel', col2: 'Pixel', alpha: float, symbol: chr = None, threshold: float = 0.005) -> 'Pixel':
    #     '''
    #         alpha: float = 0-1
    #         threshold: float = 0-1
    #     '''
        
    #     dvas = ((abs(col2.r - col1.r) + abs(col2.g - col1.g) + abs(col2.b - col1.b)) / 3) / 255
        
    #     if dvas < threshold:
    #         return Pixel(*col2.getRGB())
    #     else:
    #         return Pixel(
    #             round(col1.r * (1 - alpha) + col2.r * alpha), 
    #             round(col1.g * (1 - alpha) + col2.g * alpha), 
    #             round(col1.b * (1 - alpha) + col2.b * alpha),
    #             symbol if symbol is not None else col1.symbol
    #         )
    
    # def mix(self, col, alpha: float, symbol: chr = None, threshold: float = 0.005) -> 'Pixel':
    #     return Pixel.mixStatic(self, col, alpha, symbol, threshold)
    
    @property
    def ANSII(self) -> str:
        return f'{'⌂' if GVars.DEBUG_SHOW_ANSIICOLOR_CHARS else ''}{self.ANSIICol}{self.symbol}'
    
    @property
    def ANSIICol(self) -> str:
        if self.back_color is None:
            if self.front_color is None:
                return Pixel.clearANSII
            else:
                return f'\033[38;2;{self.front_color.x};{self.front_color.y};{self.front_color.z};49m'
        else:
            if self.front_color is None:
                return f'\033[48;2;{self.back_color.x};{self.back_color.y};{self.back_color.z};39m'
            else:
                return f'\033[38;2;{self.front_color.x};{self.front_color.y};{self.front_color.z};48;2;{self.back_color.x};{self.back_color.y};{self.back_color.z}m'

    def getRGB(self) -> tuple[Vec3[int]]:
        '''
            return (front_color, back_color)
        '''
        return self.front_color, self.back_color

    @staticmethod
    def compareColors(pixel1: 'Pixel', pixel2: 'Pixel') -> bool:
        return pixel1.front_color == pixel2.front_color and pixel1.back_color == pixel2.back_color
        
    def __str__(self):
        return f'Pixel(f:{self.front_color};b:{self.back_color})'

    def copy(self) -> 'Pixel':
        return copy.deepcopy(self)

Pixel.empty = Pixel()

class Pixels:
    f_white = Pixel((255, 255, 255))
    b_white = Pixel(None, (255, 255, 255))
    f_green = Pixel((0, 255, 0))
    b_green = Pixel(None, (0, 255, 0))
    f_gray = Pixel((125, 125, 125))
    b_gray = Pixel(None, (125, 125, 125))
    f_black = Pixel((0, 0, 0))
    b_black = Pixel(None, (0, 0, 0))
    f_red = Pixel((255, 0, 0))
    b_red = Pixel(None, (255, 0, 0))
    f_blue = Pixel((0, 0, 255))
    f_yellow = Pixel((255, 255, 0))
    wt = Pixel((255, 255, 255))
