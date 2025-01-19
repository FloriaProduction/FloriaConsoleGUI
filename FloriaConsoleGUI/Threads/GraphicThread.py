import sys

from ..Classes import Buffer
from ..Threads import BaseThread
from ..Managers.WindowManager import WindowManager
from ..Graphic.Pixel import Pixel
from ..Config import Config
from .. import Func

class GraphicThread(BaseThread):
    def __init__(self):
        super().__init__((1/Config.FPS) if Config.FPS > 0 else 0)
        self._info = {}
    
    async def convertBufferPixelToStr(self, buffer: Buffer[Pixel]) -> str:
        buffer_pixels = [
            pixel if pixel is not None else Pixel.empty 
            for pixel in buffer.data
        ]
 
        pixels: list[Pixel] = \
        [
            buffer_pixels[i].ANSII if i - i // buffer.width * buffer.width == 0 or not Pixel.compareColors(buffer_pixels[i-1], buffer_pixels[i]) else buffer_pixels[i].symbol 
            #buffer_data[i].symbol
            #buffer_data[i].ANSII
            for i in range(len(buffer_pixels))
        ]
        
        return ''.join([
            ''.join(pixels[y*buffer.width : y*buffer.width+buffer.width]) + f'{Pixel.clearANSII}\n' for y in range(buffer.height)
        ])
        
        
    
    async def simulation(self):
        buffer = await WindowManager.render()
        if buffer is None:
            return
        rendered_text = await self.convertBufferPixelToStr(buffer)
        
        if Config.DEBUG_SHOW_DEBUG_DATA:
            if Func.every('update_info', 1, True):
                self._info = self.__class__._amount_simulation.getAll()
                self.__class__._amount_simulation.clearAll()
            
            Config.debug_data.update(self._info)
        
        sys.stdout.write(f'{'\n' * Config.CLEAR_LINES}{rendered_text}{'; '.join([f'{key}={value}' for key, value in Config.debug_data.items()]) if Config.DEBUG_SHOW_DEBUG_DATA else ''}\n')
    