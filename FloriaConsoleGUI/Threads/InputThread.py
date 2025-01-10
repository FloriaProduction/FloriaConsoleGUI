import asyncio

from ..Log import Log
from ..Threads import BaseThread
from ..GVars import *
from ..Managers import KeyboardManager as KeyM, posix_key


class InputThread(BaseThread):
    def __init__(self):
        super().__init__(0.01)
        
    async def simulation(self):
        await asyncio.create_task(asyncio.to_thread(KeyM.simulation))
    
    
    
    