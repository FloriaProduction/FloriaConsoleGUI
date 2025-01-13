from typing import Union
import sys
import os

from ..Log import Log
from .. import Func
from .WindowManager import WindowManager
from ..Graphic.Widgets import Widget
from ..Graphic.Windows import Window
from ..Classes import Event
from ..GVars import GVars

from ..Graphic.Windows import *
from ..Graphic.Widgets import *

class Parser:
    _file_path: Union[str, None] = None
    _file_update_time = None
    _builded_event: Event = Event()
    
    @classmethod
    def setFile(cls, path: str):
        if not os.path.exists(path):
            Log.writeWarning(f'File "{path}" not found', cls)
        
        cls._file_path = path
        cls._file_update_time = os.path.getmtime(path)
        
        WindowManager.closeAll()
        Widget.removeAll()
        
        try:
            for window_data in Func.readJson(path):
                WindowManager.openNewWindow(
                    cls.buildWindow(window_data)
                )
                
            cls._builded_event.invoke()
            Log.writeOk('windows builded!', cls)
        except:
            WindowManager.closeAll()
            Widget.removeAll()
            Log.writeError()
    
    @classmethod
    def checkUpdate(cls):
        if cls._file_path is None:
            return
        
        now_file_update_time = os.path.getmtime(cls._file_path)
        
        if now_file_update_time != cls._file_update_time:
            cls._file_update_time = now_file_update_time
            cls.setFile(cls._file_path)
    
    @classmethod
    def buildWindow(cls, window_data: dict[str, any]) -> Window:
        def parseWidgets(data: list[dict[str, any]]) -> list[Widget]:
            widgets: list[Widget] = []
            for widget_data in data:
                widget: type[Widget] = getattr(sys.modules['FloriaConsoleGUI.Graphic.Widgets'], widget_data['class'])
                widget_data.pop('class')
                for attr in widget_data:
                    if GVars.PARSER_SKIP_UNKNOWED_ANNOTATIONS and attr not in widget.__init__.__annotations__:
                        Log.writeNotice(f'widget "{widget.__name__}" attribute "{attr}" skipped', cls)
                        continue
                    
                    attr_value = widget_data[attr]
                    match attr:
                        case 'widgets':
                            widget_data[attr] = parseWidgets(attr_value)
                    
                widgets.append(widget(**widget_data))
            return widgets
                
        window: type[Window] = getattr(sys.modules['FloriaConsoleGUI.Graphic.Windows'], window_data['class'])
        
        if 'widgets' in window_data:
            window_data['widgets'] = parseWidgets(window_data['widgets'])

        return window(**window_data)
    
    @classmethod
    def get_builded_event(cls) -> Event:
        return cls._builded_event