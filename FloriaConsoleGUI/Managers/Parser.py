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
        def parseWidgets(data: list[dict[str, any]]) -> list[Widget]:
            widgets: list[Widget] = []
            for widget_data in data:
                widget: type[Widget] = getattr(sys.modules['FloriaConsoleGUI.Graphic.Widgets'], widget_data.pop('class'))
                
                for attr in widget_data:
                    if Config.PARSER_SKIP_UNKNOWED_ANNOTATIONS and attr not in widget.__init__.__annotations__:
                        Log.writeNotice(f'widget "{widget.__name__}" attribute "{attr}" skipped', cls)
                        continue
                    
                    attr_value = widget_data[attr]
                    if isinstance(attr_value, str) and attr_value in temp:
                        widget_data[attr] = temp[attr_value]
                        
                    match attr:
                        case 'widgets':
                            widget_data[attr] = parseWidgets(attr_value)
                    
                widgets.append(widget(**widget_data))
            return widgets
        
        temp: dict[str, any] = {}
        
        if cls._file_path is None:
            return
        
        now_file_update_time = os.path.getmtime(cls._file_path)
        
        if now_file_update_time != cls._file_update_time:
            cls._file_update_time = now_file_update_time
            
            WindowManager.closeAll()
            Widget.removeAll()
            
            try:
                for data in Func.readJson(cls._file_path):
                    data_class = data.pop('class')
                    match data_class:
                        case 'temp':
                            temp.update(data)
                            
                        case _:
                            window: type[Window] = getattr(sys.modules['FloriaConsoleGUI.Graphic.Windows'], data_class)
                            
                            if 'widgets' in data:
                                data['widgets'] = parseWidgets(data['widgets'])

                            WindowManager.openNewWindow(
                                window(**data)
                            )
                    
                cls.builded_event.invoke()
                Log.writeOk('windows builded!', cls)
            except:
                WindowManager.closeAll()
                Widget.removeAll()
                Log.writeError()