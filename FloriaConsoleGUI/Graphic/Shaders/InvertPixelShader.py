from typing import Union

from FloriaConsoleGUI.Classes import *
from FloriaConsoleGUI.Graphic.Pixel import *
from .BasePixelShader import BasePixelShader

class InvertPixelShader(BasePixelShader):
    def convertFunction(
        self,
        x: int, 
        y: int, 
        buffer: Buffer[Pixel], 
        pixel: Union[Pixel, None]
    ) -> Buffer[Pixel]:
        if pixel is not None:
            pixel = pixel.change(
                front_color=Vec3(*map(lambda x: 255 - x, pixel.front_color)) if pixel.front_color is not None else None,
                back_color=Vec3(*map(lambda x: 255 - x, pixel.back_color)) if pixel.back_color is not None else None
            )
            
        return pixel