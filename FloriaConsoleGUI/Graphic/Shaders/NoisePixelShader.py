from typing import Union
from time import perf_counter
from math import floor, cos, sin
from random import choice

from FloriaConsoleGUI.Classes import *
from FloriaConsoleGUI.Graphic.Pixel import *
from .BasePixelShader import BasePixelShader

class NoisePixelShader(BasePixelShader):
    def convertFunction(
        self,
        x: int, 
        y: int, 
        buffer: Buffer[Pixel],
        pixel: Union[Pixel, None]
    ) -> Buffer[Pixel]:
        if pixel is not None and pixel.back_color is None:
            pixel = pixel.change(
                back_color=choice([
                    AnsiColor.b_black,
                    AnsiColor.b_blue,
                    AnsiColor.b_green,
                    AnsiColor.b_red,
                    AnsiColor.b_white,
                    AnsiColor.b_yellow
                ])
            )
            
        return pixel