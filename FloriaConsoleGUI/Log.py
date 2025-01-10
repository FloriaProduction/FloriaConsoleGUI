from typing import Union
from traceback import format_exc

from .Graphic.Pixel import Pixel, Pixels

class Log:
    _min_state = _min_name = 0

    @classmethod
    def write(
        cls, 
        message: str, 
        state: str, 
        name: Union[str, any, None] = None, 
        message_color: Pixel = Pixels.f_gray, 
        state_color: Pixel = Pixels.f_gray, 
        name_color: Pixel = Pixels.f_gray,
        capitalize_message: bool = True
    ):
        cls._min_state = max(cls._min_state, len(state))
        
        if not isinstance(name, str) and name is not None:
            if isinstance(name, type):
                name = name.__name__
            elif isinstance(name, object):
                name = name.__class__.__name__
        cls._min_name = max(cls._min_name, len(name)) if name is not None else cls._min_name

        print(
            f'{Pixel.clearANSII}' + 
            f'{state_color.ANSIICol}{f'[{state.upper()}]'.ljust(cls._min_state + 2)}  ' + 
            (f'{name_color.ANSIICol}{f'[{name}]'.ljust(cls._min_name + 2)}  ' if name is not None else ' ') + 
            f'{message_color.ANSIICol}{message.capitalize() if capitalize_message else message}{Pixel.clearANSII}'
        )
    
    @classmethod
    def writeOk(cls, message: str, name: Union[str, None] = None):
        cls.write(message, 'ok', name, state_color=Pixels.f_green, message_color=Pixels.f_white)
    
    @classmethod
    def writeNotice(cls, message: str, name: Union[str, None] = None):
        cls.write(message, 'notice', name)
    
    @classmethod
    def writeError(cls, name: Union[str, None] = None, message: Union[str, None] = None):
        cls.write(message if message is not None else format_exc(), 'error', name, state_color=Pixels.f_red, name_color=Pixels.f_white, message_color=Pixels.f_white, capitalize_message=False)

    @classmethod
    def writeWarning(cls, message: Union[str, None] = None, name: Union[str, None] = None):
        cls.write(message if message is not None else format_exc(), 'warning', name, state_color=Pixels.f_yellow, message_color=Pixels.f_white)


