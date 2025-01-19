from typing import Union
import sys
import os

from ..Log import Log
from .. import Func
from .WindowManager import WindowManager
from ..Graphic.Widgets import Widget
from ..Graphic.Windows import Window
from ..Classes import Event
from ..Config import Config

from ..Graphic.Windows import *
from ..Graphic.Widgets import *


class Parser:
    _file_path: Union[str, None] = None
    _file_update_time: Union[float, None] = None
    builded_event: Event = Event()
    
    @classmethod
    def setFile(cls, path: str):
        if not os.path.exists(path):
            Log.writeWarning(f'File "{path}" not found', cls)
            return
        
        cls._file_path = path
        
        Log.writeOk(f'File setted', cls)
        
        cls.checkUpdate()
        
    @classmethod
    def checkUpdate(cls):
        widgets_module = 'FloriaConsoleGUI.Graphic.Widgets'
        window_module = 'FloriaConsoleGUI.Graphic.Windows'
        temp: dict[str, any] = {}
        
        def parseGraphicObject(data: list[dict[str, any]]) -> list[Union[Window, Widget]]:
            objects: list[Union[Window, Widget]] = []
            for object_data in data:
                object_class = object_data.pop('class')
                
                if object_class == 'temp':
                    temp.update(object_data)
                    continue
                
                object = Func.choiseValue(
                    getattr(sys.modules[widgets_module], object_class, None),
                    getattr(sys.modules[window_module], object_class, None)
                )
                
                if object is None:
                    raise RuntimeError()

                for key, value in tuple(object_data.items()):
                    if Config.PARSER_SKIP_UNKNOWED_ANNOTATIONS and key not in object.__init__.__annotations__:
                        object_data.pop(key)
                        Log.writeNotice(f'widget "{object.__name__}" attribute "{key}" skipped', cls)
                        continue
                    
                    if isinstance(value, str) and value in temp:
                        object_data[key] = temp[value]
                    
                    match key:
                        case 'widgets':
                            object_data[key] = parseGraphicObject(value)
                    
                objects.append(object(**object_data))
            return objects
                
        if cls._file_path is None:
            return
        
        now_file_update_time = os.path.getmtime(cls._file_path)
        
        if now_file_update_time != cls._file_update_time:
            cls._file_update_time = now_file_update_time
            
            WindowManager.closeAll()
            Widget.removeAll()
            
            try:
                for window in parseGraphicObject(Func.readJson(cls._file_path)):
                    WindowManager.openNewWindow(
                        window
                    )
                    
                cls.builded_event.invoke()
                Log.writeOk('windows builded!', cls)
            except:
                WindowManager.closeAll()
                Widget.removeAll()
                Log.writeError()