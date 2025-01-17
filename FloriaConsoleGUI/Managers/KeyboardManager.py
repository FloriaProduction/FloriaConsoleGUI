import readchar
from typing import Union, Callable

from ..Config import Config
from ..Classes import Keys
from ..Log import Log

from ..Classes.Event import Event, EventKwargs

class KeyboardManager:
    _events: dict[str, Event] = {}
    _event_binds: dict[str, set[str]] = {}
    
    _pressed_event: EventKwargs = EventKwargs()
    
    @classmethod
    def addHandlerToPressedEvent(cls, func: Callable[[any], None]):
        '''
            func like this: `func(char: chr, **kwargs) -> None`
        '''
        cls._pressed_event.add(func)
    
    @classmethod
    def registerEvent(cls, event_name: str, key: Union[str, None] = None):
        '''
            if `key` is not None then call `KeyboardManager.bindEvent`
        '''
        if event_name in cls._events:
            raise
        cls._events[event_name] = Event()
        
        Log.writeNotice(f'Event "{event_name}" registered')
        
        if key is not None:
            cls.bindEvent(event_name, key)
        
    
    @classmethod
    def bindEvent(cls, event_name: str, key: str):
        if event_name not in cls._events:
            raise
        
        if key not in cls._event_binds:
            cls._event_binds[key] = set()
            
        cls._event_binds[key].add(event_name)
        
    @classmethod
    def bind(cls, event_name: str, func: Callable[[], None]):
        cls._events[event_name].add(func)

    @classmethod
    def simulation(cls):
        key = readchar.readkey()
        if Config.DEBUG_SHOW_INPUT_KEY:
            Log.writeNotice(f'pressed {key}', cls)
        
        for key, event_names in cls._event_binds.items():
            if key == key:
                for event_name in event_names:
                    cls._events[event_name].invoke()

        cls._pressed_event.invoke(key=key)
        
        Config.debug_data['last pressed key'] = key.encode()