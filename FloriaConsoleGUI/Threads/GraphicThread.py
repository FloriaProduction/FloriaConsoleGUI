import os, sys
from typing import Union, Iterable

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
        super().__init__((1/Config.FPS) if Config.FPS > 0 else 0)
        self._info = {}
    
    async def simulation(self):
        def pixelColorLimit(pixel: Pixel) -> Pixel:
            def _f(arr: Iterable[int]) -> Iterable[int]:
                r, g, b = 255 // Config.PIXEL_RED_DEPTH, 255 // Config.PIXEL_GREEN_DEPTH, 255 // Config.PIXEL_BLUE_DEPTH
                return [
                    ((arr[0]+1) // r * r)-1,
                    ((arr[1]+1) // g * g)-1,
                    ((arr[2]+1) // b * b)-1
                ]
            
            return Pixel(
                _f(pixel.front_color) if pixel.front_color is not None else None,
                _f(pixel.back_color) if pixel.back_color is not None else None,
                pixel.symbol
            ) 
        
        buffer = await WindowManager.render()
        if buffer is None:
            return
        
        buffer_data = [
            pixel if not Config.PIXEL_COLOR_LIMIT else pixelColorLimit(pixel) if pixel is not None else Pixel.empty 
            for pixel in buffer.data
        ]
 
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
        
        sys.stdout.write(f'{'\n' * Config.CLEAR_LINES}{rendered_text}{'; '.join([f'{key}={value}' for key, value in Config.debug_data.items()]) if Config.DEBUG_SHOW_DEBUG_DATA else ''}\n')
    