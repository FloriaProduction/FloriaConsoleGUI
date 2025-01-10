import asyncio
import os
from typing import Union
import json

from .GVars import GVars
from .Threads import BaseThread, GraphicThread, SimulationThread, InputThread
from .Classes.Event import Event
from .Log import Log
from .Managers import KeyboardManager as KeyM, posix_key, WindowManager
from . import Func

class Core:
    init_event: Event = Event()
    term_event: Event = Event()
    
    init_all_event = BaseThread.init_all_event
    
    GraphicThread = None
    SimulationThread = None
    InputThread = None

    _tasks: list[asyncio.Task] = []
    
    @classmethod
    def start(cls):
        '''
            run async app
        '''
        try:
            for thread in BaseThread._threads.values():
                cls._tasks.append(GVars.ASYNC_EVENT_LOOP.create_task(thread.run(), name=thread.name))
            
            GVars.ASYNC_EVENT_LOOP.run_until_complete(asyncio.wait(cls._tasks))
        
        except KeyboardInterrupt:
            Log.writeWarning('экстренное завершение', cls)
            
        except:
            Log.writeError(cls)
            input()
                
        finally:
            for task in cls._tasks:
                task.cancel()
            GVars.ASYNC_EVENT_LOOP.run_until_complete(asyncio.wait(cls._tasks))
            GVars.ASYNC_EVENT_LOOP.stop()
            
    @classmethod
    def init(cls):
        cls.GraphicThread = GraphicThread()
        cls.SimulationThread = SimulationThread()
        cls.InputThread = InputThread()
        
        KeyM.registerEvent('_close', posix_key.CTRL_C)
        KeyM.bind('_close', BaseThread.stopAll)
        
        cls.init_event.invoke()
        Log.writeOk('Initialized', cls)
    
    @classmethod
    def term(cls):
        cls.init_event.invoke()
        Log.writeOk('Terminated', cls)
    

             