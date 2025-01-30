from sys import platform

match platform:
    case 'win32':
        UP = '\x00H'
        DOWN = '\x00P'
        LEFT = '\x00K'
        RIGHT = '\x00M'

        DELETE = '\x00S'
        BACKSPACE = '\x08'

        ENTER = '\r'

        HOME = '\x00G'
        END = '\x00O'

        CTRL_BACKSPACE = '\x7f'

    case 'linux':
        UP = '\x1b[A'
        DOWN = '\x1b[B'
        LEFT = '\x1b[D'
        RIGHT = '\x1b[C'

        DELETE = '\x1b[3~'
        BACKSPACE = '\x7f'

        ENTER = '\n'

        HOME = '\x1b[H'
        END = '\x1b[F'

        CTRL_BACKSPACE = '\x08'

    case _:
        raise RuntimeError(
            'Dont support platform'
        )

CTRL_C = '\x03'
CTRL_UP = '\x00\xc2\x8d'
CTRL_RIGHT = '\x00t'
CTRL_LEFT = '\x00s'
CTRL_DOWN = '\x00\xc2\x91'

CTRL_DELETE = '\x00\xc2\x93'

SPACE = ' '
TAB = '\t'
