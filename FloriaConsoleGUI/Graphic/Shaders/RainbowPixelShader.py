from typing import Union, overload
from time import perf_counter
from math import floor, cos, sin

from FloriaConsoleGUI.Classes import *
from FloriaConsoleGUI.Graphic.Pixel import *
from .BasePixelShader import BasePixelShader

class RainbowPixelShader(BasePixelShader):
    @overload
    def __init__(
        self,
        size: float = 1,
        speed: float = 1,
        direction: Orientation = None,
        **kwargs
    ): ...
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._t1 = perf_counter()
        self.size = kwargs.get('size', 1)
        self.speed = kwargs.get('speed', 1)
        self.direction = kwargs.get('direction')
    
    def convertFunction(
        self,
        x: int, 
        y: int, 
        buffer: Buffer[Pixel],
        pixel: Union[Pixel, None]
    ) -> Buffer[Pixel]:
        if pixel is not None and pixel.back_color is None:
            indent = (self._t1 - perf_counter()) * self.speed
            
            x += indent
            
            # match self.direction:
            #     case Orientation.vertical:
            #         y += indent
                
            #     case Orientation.horizontal:
            #         x += indent

            #     case None:
            #         x += indent
            #         y += indent
            
            pixel = pixel.change(
                back_color=Vec3(
                    floor((
                        cos(x*self.size)
                        +1)*127
                    ),
                    floor((
                        cos((x*self.size)+2.0944)
                        +1)*127
                    ),
                    floor((
                        cos((x*self.size)+4.1888)
                        +1)*127
                    )
                )
            )
            
        return pixel

