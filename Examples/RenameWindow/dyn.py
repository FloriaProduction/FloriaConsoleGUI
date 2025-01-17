from FloriaConsoleGUI import *
from FloriaConsoleGUI.Managers import *
from FloriaConsoleGUI.Graphic.Widgets import *
from FloriaConsoleGUI.Graphic.Windows import *


@Parser.builded_event.dec
def builded():
    window_main: TitledWindow = WindowManager.getByName('main')
    textbox: TextBox = Widget.getByName('Textbox_name')
    button_rename: Button = Widget.getByName('Button_rename')
    
    if button_rename and window_main and textbox:
        @button_rename.pressed_event.dec
        def button_rename_pressed():
            window_main.title = textbox.text
