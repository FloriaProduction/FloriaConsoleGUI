import asyncio
import os
from typing import Union
import importlib
import time

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
    
    GraphicThread = GraphicThread()
    SimulationThread = SimulationThread()
    InputThread = InputThread()

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
            Log.writeWarning('Emergency termination', cls)
            
        except:
            Log.writeError(cls)
            input('Press to continue...')
                
        finally:
            for task in cls._tasks:
                task.cancel()
            GVars.ASYNC_EVENT_LOOP.run_until_complete(asyncio.wait(cls._tasks))
            GVars.ASYNC_EVENT_LOOP.stop()
            
    @classmethod
    def init(cls):
        KeyM.registerEvent('_close', posix_key.CTRL_C)
        KeyM.bindEvent('_close', '\x00k') # alt+f4
        KeyM.bind('_close', BaseThread.stopAll)
        
        cls.init_event.invoke()
        Log.writeOk('Initialized', cls)
    
    @classmethod
    def term(cls):
        cls.init_event.invoke()
        Log.writeOk('Terminated', cls)
    
    _dynamic_modules: dict[str, dict[str, any]] = {}
    @classmethod
    def addDynamicModule(cls, path: str, name: str):
        if path in cls._dynamic_modules:
            raise ValueError(f'Module "{path}" already exists')
        
        if not os.path.exists(path):
            raise ValueError(f'File "{path}" not exists')
        
        if GVars.WRITE_WARNING_DYNAMIC_MODULE and len(cls._dynamic_modules) == 0:
            Log.writeWarning(
                '\nThis tool is unstable due to its features and may lead to errors\nIt is strongly recommended to only change variables inside the module\nNo complex logic', cls
            )
            time.sleep(0.5)
            
        
        cls._dynamic_modules[path] = {
            'mtime': os.path.getmtime(path),
            'name': name,
            'module': importlib.import_module(name)
        }
    
    @classmethod
    def checkDynamicModules(cls):
        for path, data in cls._dynamic_modules.items():
            if not os.path.exists(path):
                continue
            
            os.path.dirname
            
            last_mtime = os.path.getmtime(path)
            if data['mtime'] == last_mtime:
                continue
            
            data['module'] = importlib.reload(data['module'])
            data['mtime'] = last_mtime
            
            Log.writeOk(f'module "{path}" updated')
            
    

             