from typing import Union, Iterable, overload

from ..Classes import Vec3, AnsiColor
from ..Config import Config


class Pixel:
    empty: 'Pixel' = None
    ANSI_clear = f'\033[0m'
    
    def __init__(
        self, 
        front_color: Union[Iterable[int], AnsiColor, None] = None, 
        back_color: Union[Iterable[int], AnsiColor, None] = None, 
        symbol: chr = None
    ):
        self.front_color: Union[Vec3[int], AnsiColor, None] = Vec3(*front_color) if isinstance(front_color, Iterable) else front_color
        self.back_color: Union[Vec3[int], AnsiColor, None] = Vec3(*back_color) if isinstance(back_color, Iterable) else back_color
        self.symbol = symbol if symbol is not None else ' '
        
        if isinstance(self.front_color, int):
            raise

    
    @staticmethod
    def fromRGB(br: int, bg: int, bb: int, symbol: chr = None) -> 'Pixel':
        return Pixel(back_color=Vec3(br, bg, bb), symbol=symbol)
    
    @staticmethod
    @overload
    def changePixel(
        pixel: Union['Pixel', None], 
        symbol: chr, 
        front_color: Vec3, 
        back_color: Vec3
    ) -> Union['Pixel', None]: ...

    @staticmethod
    def changePixel(pixel: Union['Pixel', None], **kwargs):
        '''
            create a copy of the pixel and change it
        '''
        
        new_pixel = pixel.copy() if pixel is not None else Pixel.empty.copy()
        
        if 'symbol' in kwargs:
            new_pixel.symbol = kwargs.get('symbol')
        
        if 'front_color' in kwargs:
            new_pixel.front_color = kwargs.get('front_color')
        
        if 'back_color' in kwargs:
            new_pixel.back_color = kwargs.get('back_color') 
        
        return new_pixel
    
    @overload
    def change(
        self, 
        symbol: chr = None, 
        front_color: Vec3 = None, 
        back_color: Vec3 = None
    ) -> Union['Pixel', None]: ...
    
    def change(self, **kwargs) -> Union['Pixel', None]:
        return Pixel.changePixel(self, **kwargs)
        
    
    
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
    def ANSI(self) -> str:
        return f'{self.ANSI_color}{self.symbol}'
    
    @property
    def ANSI_color(self) -> str:
        if self.back_color is None and self.front_color is None:
            return self.ANSI_clear
        return f'\033[{self.ANSI_front_color};{self.ANSI_back_color}m'
        
    @property
    def ANSI_back_color(self) -> str:
        if self.back_color is None:
            return f'49'
        if isinstance(self.back_color, AnsiColor):
            return f'{self.back_color.value}'
        return f'48;2;{';'.join(map(str, self.back_color))}'
    
    @property
    def ANSI_front_color(self) -> str:
        if self.front_color is None:
            return f'39'
        if isinstance(self.front_color, AnsiColor):
            return f'{self.front_color.value}'
        return f'38;2;{';'.join(map(str, self.front_color))}'

    def getRGB(self) -> tuple[Vec3[int]]:
        '''
            return (front_color, back_color)
        '''
        return self.front_color, self.back_color

    @staticmethod
    def compareColors(pixel1: 'Pixel', pixel2: 'Pixel') -> bool:
        return pixel1.front_color == pixel2.front_color and pixel1.back_color == pixel2.back_color
    
    def getColors(self) -> tuple[Vec3, Vec3]:
        return (
            self.front_color,
            self.back_color
        )
    
    def __str__(self):
        return f'Pixel(f:{self.front_color};b:{self.back_color})'

    def copy(self) -> 'Pixel':
        return self.__class__(
            self.front_color,
            self.back_color,
            self.symbol
        )

Pixel.empty = Pixel()

class Pixels:
    f_white = Pixel(AnsiColor.f_white)
    b_white = Pixel(None, AnsiColor.b_white)
    f_green = Pixel(AnsiColor.f_green)
    b_green = Pixel(None, AnsiColor.b_green)
    f_light_gray = Pixel((192, 192, 192))
    f_gray = Pixel((128, 128, 128))
    f_dark_gray = Pixel((64, 64, 64))
    b_light_gray = Pixel(None, (192, 192, 192))
    b_gray = Pixel(None, (128, 128, 128))
    b_dark_gray = Pixel(None, (64, 64, 64))
    f_black = Pixel(AnsiColor.f_black)
    b_black = Pixel(None, AnsiColor.b_black)
    f_red = Pixel(AnsiColor.f_red)
    b_red = Pixel(None, AnsiColor.b_red)
    f_blue = Pixel(AnsiColor.f_blue)
    b_blue = Pixel(None, AnsiColor.b_blue)
    f_yellow = Pixel(AnsiColor.f_yellow)
    b_yellow = Pixel(None, AnsiColor.b_yellow)
    white_black = Pixel(AnsiColor.f_white)
    black_white = Pixel(AnsiColor.f_black, AnsiColor.b_white)
