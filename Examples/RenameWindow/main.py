from FloriaConsoleGUI import *
from FloriaConsoleGUI.Managers import *
from FloriaConsoleGUI.Graphic.Widgets import *
from FloriaConsoleGUI.Graphic.Windows import *
from FloriaConsoleGUI.Graphic import *
from FloriaConsoleGUI.Classes import *


@Core.initialized_all_threads_event.dec
def _():
    Core.setConsoleName('Example TextBox')
    
    SoundManager.load('./data/sounds/sounds.json')

    WindowManager.openNewWindow(
        TitledWindow(
            name='main',
            offset_pos=[1, 0, 0],
            frame=True,
            title=' Example CheckBox ',
            title_anchor=Anchor.center,
            padding=[1, 1, 1, 1],
            direction=Orientation.vertical,
            gap=1,
            title_style=1,
            widgets=[
                Container(
                    direction=Orientation.horizontal,
                    gap=1,
                    widgets=[
                        Label(
                            text='name:'
                        ),
                        TextBox(
                            name='Textbox_name',
                            text_max_size=[15, 1]
                        )
                    ]
                ),
                Button(
                    name='Button_rename',
                    text='Rename',
                    clear_pixel=Pixels.black_white,
                    select_clear_pixel=Pixels.b_blue,
                    padding=[1, 1, 1, 1],
                    min_size=[20, None]
                ),
                Button(
                    text='Close',
                    clear_pixel=Pixels.black_white,
                    select_clear_pixel=Pixels.b_blue,
                    padding=[1, 1, 1, 1],
                    min_size=[20, None],
                    on_press_functions=[
                        Core.stop
                    ]
                )
            ]
        )
    )
    
    window_main: TitledWindow = WindowManager.getByName('main')
    textbox: TextBox = Widget.getByName('Textbox_name')
    button_rename: Button = Widget.getByName('Button_rename')
    
    @button_rename.pressed_event.dec
    def _():
        window_main.title = textbox.text


@KeyboardManager.pressed_event.dec
def _():
    SoundManager.play('key_down')


if __name__ == "__main__":
    Core.init()
    Core.start()
    Core.term()