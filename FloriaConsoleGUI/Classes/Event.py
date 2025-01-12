import asyncio
from typing import Callable

class Event:
    def __init__(self, funcs: list[Callable[[], None]] = []):
        self._funcs: set[Callable[[any], None]] = set(funcs) if isinstance(funcs, list | tuple) else set([funcs])

    def add(self, func: Callable[[], None]):
        self._funcs.add(func)
        
    def invoke(self):
        for func in self._funcs:
            res = func()
            if asyncio.iscoroutine(res):
                raise 
                
    async def invokeAsync(self):
        for func in self._funcs:
            res = func()
            if asyncio.iscoroutine(res):
                await res


class EventKwargs(Event):
    def add(self, func: Callable[[any], None]):
        super().add(func)
    
    def invoke(self, **kwargs):
        for func in self._funcs:
            res = func(**kwargs)
            if asyncio.iscoroutine(res):
                raise 
    
    async def invokeAsync(self, **kwargs):
        for func in self._funcs:
            res = func(**kwargs)
            if asyncio.iscoroutine(res):
                await res