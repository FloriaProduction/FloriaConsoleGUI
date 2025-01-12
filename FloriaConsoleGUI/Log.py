from typing import Union
from traceback import format_exc

class Log:
    _min_state = _min_name = 0

    @classmethod
    def write(
        cls, 
        message: str, 
        state: str, 
        name: Union[str, any, None] = None, 
        message_color: str = '\033[38;2;125;125;125;49m', 
        state_color: str = '\033[38;2;125;125;125;49m', 
        name_color: str = '\033[38;2;125;125;125;49m',
        capitalize_message: bool = True
    ):
        cls._min_state = max(cls._min_state, len(state))
        
        if not isinstance(name, str) and name is not None:
            if isinstance(name, type):
                name = name.__name__
            elif isinstance(name, object):
                name = name.__class__.__name__
        cls._min_name = max(cls._min_name, len(name)) if name is not None else cls._min_name

        if capitalize_message:
            message = message[0].capitalize() + message[1:]
        
        print(
            '\033[0m' + 
            f'{state_color}{f'[{state.upper()}]'.ljust(cls._min_state + 2)}  ' + 
            (f'{name_color}{f'[{name}]'.ljust(cls._min_name + 2)}  ' if name is not None else '') + 
            f'{message_color}{message}\033[0m'
        )
    
    @classmethod
    def writeOk(cls, message: str, name: Union[str, None] = None):
        cls.write(
            message, 
            'ok', 
            name, 
            state_color='\033[32;49m', 
            message_color='\033[37;49m'
        )
    
    @classmethod
    def writeNotice(cls, message: str, name: Union[str, None] = None):
        cls.write(
            message, 
            'notice', 
            name
        )
    
    @classmethod
    def writeError(cls, name: Union[str, None] = None, message: Union[str, None] = None):
        cls.write(
            message if message is not None else format_exc(), 
            'error', 
            name, 
            state_color='\033[31;49m', 
            name_color='\033[37;49m', 
            message_color='\033[37;49m', 
            capitalize_message=False
        )

    @classmethod
    def writeWarning(cls, message: Union[str, None] = None, name: Union[str, None] = None):
        cls.write(
            message if message is not None else format_exc(), 
            'warning', 
            name, 
            state_color='\033[33;49m', 
            message_color='\033[37;49m'
        )


