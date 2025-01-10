import asyncio
from typing import Callable


class Event:
    def __init__(self, funcs: list[Callable[[], None]] = []):
        self._funcs: list[Callable[[], None]] = list(funcs) if isinstance(funcs, list | tuple) else [funcs]

    def add(self, func: Callable[[], None]):
        self._funcs.append(func)
        
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
