from FloriaConsoleGUI import *
from FloriaConsoleGUI.Classes import *
from FloriaConsoleGUI.Graphic import *
from FloriaConsoleGUI.Graphic.Widgets import *
from FloriaConsoleGUI.Graphic.Windows import *
from FloriaConsoleGUI.Managers import *
from FloriaConsoleGUI.Graphic.Shaders import *


@Core.initialized_all_threads_event.dec
def _():
    def renameWindow(window_name: str):
        titledwindow1: TitledWindow = WindowManager.getByName('titledwindow1')
        if titledwindow1:
            titledwindow1.title = window_name
    
    SoundManager.load('./data/sounds/sounds.json')
    KeyboardManager.pressed_event.add(
        lambda: SoundManager.play('key_down')
    )
    
    WindowManager.openNewWindow(
        TitledWindow(
            name='titledwindow1',
            title='Example RenameWindow',
            title_anchor=Anchor.center,
            title_style=1,
            offset_pos=[1, 0, 0],
            padding=[1, 1, 1, 1],
            min_size=[50, None],
            size_by_objects=True,
            objects_direction=Orientation.vertical,
            gap=1,
            widgets=[
                TextBox(
                    name='textbox1',
                    
                    placeholder='Window name',
                    max_size=[52 - 1, 1],
                ),
                Button(
                    name='button1',
                    
                    text='Rename',
                    padding=[1, 1, 1, 1],
                    size_hint=[1, None]
                ),
                Button(
                    name='button2',
                    
                    text='close',
                    padding=[1, 1, 1, 1],
                    size_hint=[1, None]
                )
            ]
        )
    )
    
    textbox1: TextBox = Widget.getByName('textbox1')
    button1: Button = Widget.getByName('button1')
    button2: Button = Widget.getByName('button2')
    
    textbox1.press_enter_event.add(
        lambda: renameWindow(textbox1.text)
    )
    button1.press_enter_event.add(
        lambda: renameWindow(textbox1.text)
    )
    button2.press_enter_event.add(
        Core.stop
    )
    

if __name__ == '__main__':
    Core.init(
        change_current_directory=__file__
    )
    Core.run()
    Core.term()