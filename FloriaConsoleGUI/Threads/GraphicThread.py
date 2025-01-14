import os, sys

from ..Log import Log
from ..Threads import BaseThread
from ..Managers.WindowManager import WindowManager
from ..Graphic.Pixel import Pixel, Pixels
from ..Graphic.Widgets import Widget
from ..Graphic.Windows import Window
from ..Config import Config
from .. import Func

class GraphicThread(BaseThread):
    def __init__(self):
        super().__init__(1/Config.FPS)
        self._info = {}
    
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
            for i in range(len(buffer_data))
        ]
        
        rendered_text = ''.join([
            ''.join(pixels[y*buffer.width : y*buffer.width+buffer.width]) + f'{Pixel.clearANSII}\n' for y in range(buffer.height)
        ])
        
        if Config.DEBUG_SHOW_DEBUG_DATA:
            if Func.every('update_info', 1, True):
                self._info = self.__class__._amt_sim.getAll()
                self.__class__._amt_sim.clearAll()
            
            Config.debug_data.update(self._info)
        
        sys.stdout.write(f'{'\n' * Config.CLEAR_LINES}{rendered_text}{'; '.join([f'{key}={value}' for key, value in Config.debug_data.items()]) if Config.DEBUG_SHOW_DEBUG_DATA else ''}')
    