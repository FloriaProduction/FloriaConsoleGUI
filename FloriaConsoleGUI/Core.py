import asyncio
import os
import sys
from typing import Union
import importlib
import time



from .Config import Config
from .Threads import BaseThread, GraphicThread, SimulationThread, InputThread
from .Classes.Event import Event
from .Log import Log
from .Managers import KeyboardManager as KeyM, WindowManager, Keys
from . import Func

class Core:   
    init_event: Event = Event()
    term_event: Event = Event()
    
    init_all_event = BaseThread.init_all_event
    
    GraphicThread = GraphicThread()
    SimulationThread = SimulationThread()
    InputThread = InputThread()

    _inited = False
    _tasks: list[asyncio.Task] = []
    
    @classmethod
    def start(cls):
        '''
            run async app
        '''
        try:
            if cls._inited is False:
                raise RuntimeError('Core was not initialized')
            
            for thread in BaseThread._threads.values():
                cls._tasks.append(Config.ASYNC_EVENT_LOOP.create_task(thread.run(), name=thread.name))
            
            Config.ASYNC_EVENT_LOOP.run_until_complete(asyncio.wait(cls._tasks))
        
        except KeyboardInterrupt:
            Log.writeWarning('Emergency termination', cls)
            
        except:
            Log.writeError(cls)
            input('Press to continue...')
                
        finally:
            for task in cls._tasks:
                task.cancel()
            Config.ASYNC_EVENT_LOOP.run_until_complete(asyncio.wait(cls._tasks))
            Config.ASYNC_EVENT_LOOP.stop()
            
    @classmethod
    def init(cls):
        if Config.CORE_MODIFY_WIN_REGEDIT and sys.platform == 'win32':
            import winreg
            
            try:
                reg_value = winreg.QueryValueEx(
                    winreg.OpenKey(
                        winreg.HKEY_CURRENT_USER, 
                        'Console', 
                        access=winreg.KEY_READ
                    ), 
                    'VirtualTerminalLevel'
                )
            except:
                reg_value = None
            
            if reg_value is None or reg_value[0] != 1:
                winreg.SetValueEx(
                    winreg.OpenKey(
                        winreg.HKEY_CURRENT_USER, 
                        'Console', 
                        access=winreg.KEY_SET_VALUE
                    ), 
                    'VirtualTerminalLevel',
                    0,
                    winreg.REG_DWORD,
                    1
                )
                
                input('Regedit has been modified, please restart the application\nPress to close...')
                exit()
                
        # KeyM.registerEvent('_close', Keys.CTRL_C)
        # KeyM.bind('_close', BaseThread.stopAll)
        
        cls.SimulationThread.delay = (1/Config.SPS) if Config.SPS > 0 else 0
        cls.GraphicThread.delay = (1/Config.FPS) if Config.FPS > 0 else 0
        
        cls.init_event.invoke()
        
        cls._inited = True
        Log.writeOk('Initialized', cls)
    
    @classmethod
    def term(cls):
        if cls._inited is False:
            raise RuntimeError('Core was not initialized')
        
        cls.init_event.invoke()
        
        cls._inited = False
        Log.writeOk('Terminated', cls)
    
    _dynamic_modules: dict[str, dict[str, any]] = {}
    @classmethod
    def addDynamicModule(cls, path: str, name: str):
        if path in cls._dynamic_modules:
            raise ValueError(f'Module "{path}" already exists')
        
        if not os.path.exists(path):
            raise ValueError(f'File "{path}" not exists')
        
        if Config.CORE_WRITE_WARNING_DYNAMIC_MODULE and len(cls._dynamic_modules) == 0:
            Log.writeWarning(
                '\nThis tool is unstable due to its features and may lead to errors\nIt is strongly recommended to only change variables inside the module\nNo complex logic', cls
            )
            time.sleep(0.5)
            
        
        cls._dynamic_modules[path] = {
            'mtime': os.path.getmtime(path),
            'name': name,
            'module': importlib.import_module(name)
        }
        Log.writeOk(f'module "{path}" added', cls)
        
    @classmethod
    def popDynamicModule(cls, path: str):
        if cls._dynamic_modules.pop(path, None) is not None:
            Log.writeOk(f'module "{path}" removed', cls)
    
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
            
    

             