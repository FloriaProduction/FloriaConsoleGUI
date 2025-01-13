import os, sys

from ..Log import Log
from ..Threads import BaseThread
from ..Managers import WindowManager
from ..Graphic import Pixel, Pixels
from ..Graphic.Widgets import Widget
from ..Graphic.Windows import Window
from ..GVars import *

class GraphicThread(BaseThread):
    def __init__(self):
        super().__init__(1/GVars.FPS)
    
    async def simulation(self):
        buffer = WindowManager.render()
        if buffer is None:
            return
        
        buffer_data = [pixel if pixel is not None else Pixel.empty for pixel in buffer.data]
        
        pixels: list[Pixel] = \
        [
            buffer_data[i].ANSII if i - i // buffer.width * buffer.width == 0 or not Pixel.compareColors(buffer_data[i-1], buffer_data[i]) else buffer_data[i].symbol 
            #buffer_data[i].symbol
            #buffer_data[i].ANSII
                for i in range(len(buffer))
        ]
        
        rendered_text = ''.join([
            ''.join(pixels[y*buffer.width : y*buffer.width+buffer.width]) + f'{Pixel.clearANSII}\n' for y in range(buffer.height)
        ])
        
        # os.system('cls')
        sys.stdout.write('\n' * GVars.CLEAR_LINES + rendered_text)
    