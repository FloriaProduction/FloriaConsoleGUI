import readchar
from typing import Union, Callable

from ..Config import Config
from ..Log import Log

from ..Classes.Event import Event, EventKwargs

class KeyboardManager:
    _events: dict[str, Event] = {}
    _event_binds: dict[str, set[str]] = {}
    
    pressed_event: EventKwargs = EventKwargs()
    
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
        readkey = readchar.readkey()
        if Config.DEBUG_SHOW_INPUT_KEY:
            Log.writeNotice(f'pressed {readkey}', cls)
        
        for key, event_names in cls._event_binds.items():
            if readkey == key:
                for event_name in event_names:
                    cls._events[event_name].invoke()

        cls.pressed_event.invoke(key=readkey)
        
        Config.debug_data[cls.__name__] = readkey.encode()