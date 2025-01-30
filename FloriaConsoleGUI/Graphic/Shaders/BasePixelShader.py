from typing import Union

from ..Pixel import *
from ...Classes import *

class BasePixelShader:
    def __init__(self, **kwargs):
        pass
    
    def convertFunction(
        self,
        x: int,
        y: int,
        buffer: Buffer[Pixel],
        pixel: Union[Pixel, None]
    ) -> Buffer[Pixel]:
        return pixel