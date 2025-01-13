import asyncio
from typing import Callable, Iterable

from ..Log import Log

class Event:
    def __init__(self, *args: Callable[[any], None], **kwargs):
        '''
            error_ignored: bool = False
        '''
        self._funcs: dict[str, Callable[[any], None]] = {}
        for func in args:
            self.add(func)
            
        self._error_ignored = kwargs.get('error_ignored', False)
    
    def dec(self, func, *args, **kwargs):
        '''
            Add func in event
        '''
        self.add(func)
     
    def add(self, *args: Callable[[], None]):
        for func in args:
            if not issubclass(func.__class__, Callable):
                raise ValueError('The resulting function is not such')
            self._funcs[f'{func.__module__}.{func.__name__}_{tuple(func.__annotations__.keys())}'] = func

    def invoke(self, *args, **kwargs):
        for func in self._funcs.values():
            try:
                res = func(*args, **kwargs)
                if asyncio.iscoroutine(res):
                    raise 
                
            except Exception as ex:
                if not self._error_ignored:
                    raise ex
                Log.writeError()
                
                
    async def invokeAsync(self, *args, **kwargs):
        for func in self._funcs.values():
            try:
                res = func(*args, **kwargs)
                if asyncio.iscoroutine(res):
                    await res
                    
            except Exception as ex:
                if not self._error_ignored:
                    raise ex
                Log.writeError()


class EventKwargs(Event):
    def add(self, func: Callable[[any], None]):
        super().add(func)
    
    def invoke(self, **kwargs):
        super().invoke(**kwargs)
                
    async def invokeAsync(self, **kwargs):
        super().invokeAsync(**kwargs)