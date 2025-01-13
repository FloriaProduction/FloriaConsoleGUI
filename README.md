Framework for console GUI apps

## Установка

Установить через pip:

```bash 
pip install FloriaConsoleGUI --upgrade
```

Или скачать исходный код из [PyPi](https://pypi.org/project/FloriaConsoleGUI/)

## Использование

Рекомендуется писать код только в самом python

### Пример обычного использования:

`main.py`:

```python
from random import random as rdf

from FloriaConsoleGUI.Core import Core
from FloriaConsoleGUI.GVars import GVars
from FloriaConsoleGUI.Graphic.Widgets import *
from FloriaConsoleGUI.Graphic.Windows import *
from FloriaConsoleGUI.Managers import *

@Core.init_all_event.dec
def init():
    WindowManager.openNewWindow(
        TitledWindow(
            size=(20, 10),
            frame=True,
            title=' Example ',
            
            widgets=[
                Label(
                    text='hello world!',
                    name='label'
                )
            ]
        )
    )

@Core.SimulationThread.sim_event.dec
def simulation():
    label: Label = Widget.getByName('label')
    if label is not None:
        label.text = f'{rdf():.4f}'


if __name__ == '__main__': 
    GVars.FPS = 30
    GVars.SPS = 30
    
    Core.init()
    
    Core.start()
    Core.term()
```

Однако, для удобства есть динамическое обновление:
- .json - для древа
- .py - для скриптов (не рекомендуется из-за специфики реализации)

Не обязательно использовать сразу оба

### Пример с динамическим обновлением:

`main.py`:

```python
from FloriaConsoleGUI.Core import Core
from FloriaConsoleGUI.GVars import GVars
from FloriaConsoleGUI.Managers import Parser


@Core.init_all_event.dec
def init():
    Core.addDynamicModule('dyn.py', 'dyn')
    Parser.setFile('./dyn.json')

@Core.SimulationThread.sim_event.dec
def simulation():
    Core.checkDynamicModules()
    Parser.checkUpdate()    


if __name__ == '__main__': 
    GVars.FPS = 30
    GVars.SPS = 30
    
    Core.init()
    
    Core.start()
    Core.term()
```

`dyn.py`:

```python
from random import random as rdf

from FloriaConsoleGUI import *
from FloriaConsoleGUI.Graphic.Widgets import *


@Core.SimulationThread.sim_event.dec
def simulation():
    label: Label = Widget.getByName('label')
    if label is not None:
        label.text = f'{rdf():.4f}'
```

`dyn.json`:

```json
[
    {
        "class": "TitledWindow",
        
        "size": [20, 10],
        "frame": true,
        "title": " Example ",

        "widgets": [
            {
                "class": "Label",
                "name": "label",

                "text": "hello world!"
            }
        ]
    }
]
```

### Результат:

![example window](https://github.com/FloriaProduction/FloriaConsoleGUI.github.io/blob/main/static/images/Example.png?raw=true)

## Документация

На данный момент [документация](https://FloriaConsoleGUI.github.io) разрабатывается...