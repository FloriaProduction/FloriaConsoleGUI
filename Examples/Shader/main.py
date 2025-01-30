from FloriaConsoleGUI import *
from FloriaConsoleGUI.Classes import *
from FloriaConsoleGUI.Graphic import *
from FloriaConsoleGUI.Graphic.Widgets import *
from FloriaConsoleGUI.Graphic.Windows import *
from FloriaConsoleGUI.Managers import *
from FloriaConsoleGUI.Graphic.Shaders import *


@Core.initialized_all_threads_event.dec
def _():
    WindowManager.openNewWindow(
        TitledWindow(
            title='Example Shader',
            title_anchor=Anchor.center,
            title_style=1,
            offset_pos=[1, 0, 0],
            padding=[1, 1, 1, 1],
            min_size=[50, None],
            size_by_objects=True,
            objects_direction=Orientation.vertical,
            gap=1,
            shader=RainbowPixelShader(size=0.05, speed=20),
            widgets=[
                Button(
                    text='Button',
                    padding=[1, 1, 1, 1],
                    size_hint=[1, None]
                ),
                Button(
                    text='Close',
                    padding=[1, 1, 1, 1],
                    size_hint=[1, None],
                    press_functions=[
                        Core.stop
                    ]
                )
            ]
        )
    )
    

if __name__ == '__main__':
    Core.init(
        change_current_directory=__file__
    )
    Core.run()
    Core.term()