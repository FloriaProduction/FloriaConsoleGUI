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
        
        ansii_pixels = [
            f'{'ᵃ' if Config.DEBUG_SHOW_ANSIICOLOR_CHARS else ''}{pixel.ANSI}' 
                if (pixel.front_color != previous_pixel.front_color and pixel.back_color != previous_pixel.back_color) else
            f'\033[{pixel.ANSI_front_color}m{'ᶠ' if Config.DEBUG_SHOW_ANSIICOLOR_CHARS else ''}{pixel.symbol}' 
                if pixel.front_color != previous_pixel.front_color else
            f'\033[{pixel.ANSI_back_color}m{'ᵇ' if Config.DEBUG_SHOW_ANSIICOLOR_CHARS else ''}{pixel.symbol}' 
                if pixel.back_color != previous_pixel.back_color else
            f'{pixel.symbol}' 
            
            for i, pixel, previous_pixel in 
            [
                (
                    i,
                    buffer_pixels[i], 
                    buffer_pixels[i-1]
                ) for i in range(len(buffer_pixels))
            ]
        ]
        
        return ''.join([
            ''.join(ansii_pixels[y*buffer.width : y*buffer.width+buffer.width]) + f'{Pixel.ANSI_clear}\n' 
            for y in range(buffer.height)
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
            Config.debug_data['len_rendered_text'] = len(rendered_text)
            Config.debug_data['len_pixels'] = len(buffer)
        
        
        sys.stdout.write(
            f'{'\n' * Config.CLEAR_LINES}' + 
            f'{rendered_text}' + 
            f'\n{'\n'.join([f'{key}={value}' for key, value in Config.debug_data.items()]) if Config.DEBUG_SHOW_DEBUG_DATA else ''}'
        )
    