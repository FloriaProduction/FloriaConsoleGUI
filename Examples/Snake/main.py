from typing import Union, Iterable, overload
from random import randint as rd

from FloriaConsoleGUI import *
from FloriaConsoleGUI.Classes import Anchor, Buffer, Vec2, Vec3, Vec4
from FloriaConsoleGUI.Classes import *
from FloriaConsoleGUI.Graphic import *
from FloriaConsoleGUI.Graphic.Widgets import *
from FloriaConsoleGUI.Graphic.Windows import *
from FloriaConsoleGUI.Managers import *


class SnakeWidget(InteractiveWidget):
    @overload
    def __init__(
        self,
        snake_pixel: Pixel | tuple[Vec3[int] | Iterable[int], Vec3[int] | Iterable[int], str] | str = None, 
        snake_speed: float = 2.5, # number moves in second
        snake_length: int = 3,
        apple_pixel: Pixel | tuple[Vec3[int] | Iterable[int], Vec3[int] | Iterable[int], str] | str = None, 
        text_pixel: Pixel | tuple[Vec3[int] | Iterable[int], Vec3[int] | Iterable[int], str] | str = None, 
        size: Vec2[int] | Iterable[int] = None, 
        min_size: Vec2[int | None] | Iterable[int | None] | None = None,
        max_size: Vec2[int | None] | Iterable[int | None] | None = None, 
        size_hint: Union[Iterable[Union[float, None]], None] = None,
        padding: Vec4[int] | Iterable[int] = None, 
        offset_pos: Vec3[int] | Iterable[int] = None, 
        pos_hint: Union[Iterable[Union[int, None]], None] = None,
        clear_pixel: Union[Pixel, tuple[Iterable[int], Iterable[int], str], str] = None,
        selected_clear_pixel: Union[Pixel, tuple[Iterable[int], Iterable[int], str], str] = None,
        name: str = 'snake_game',
        **kwargs
    ): ...
    
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self._snake_length_initial: int = kwargs.get('snake_length', 3)
        
        self._snake_delay = 1 / kwargs.get('snake_speed', 2.5)
        self._snake_pixel = Converter.toPixel(kwargs.get('snake_pixel'), default=Pixel(AnsiColor.f_green, None, '█'))
        self._snake_position: Vec2[int] = None
        self._snake_parts: dict[Vec2[int], Pixel] = None
        self._snake_length: int = None
        self._snake_direction: int = 0 # w a s d  -  0 1 2 3
        self._snake_is_dead: bool = False
        self.reloadSnake()
        
        self._apple_position: Vec2[int] = None
        self._apple_pixel = Converter.toPixel(kwargs.get('apple_pixel'), default=Pixel(AnsiColor.f_red, None, '♥'))
        self.createApple()

        self._text_pixel = Converter.toPixel(kwargs.get('text_pixel'), default=Pixels.black_white)

    def reloadSnake(self):
        self._snake_position = Vec2(self.width//2, self.height//2)
        self._snake_parts = {
            self._snake_position.toTuple(): self._snake_pixel.copy()
        }
        self._snake_length = self._snake_length_initial
        self._snake_is_dead = False
        
        self.setFlagRefresh()

    def createApple(self):
        self._apple_position = None # костыль для эмуляции do-while
        while self._apple_position == None or self._apple_position.toTuple() in self._snake_parts:
            self._apple_position = Vec2(
                rd(0, self.width-1),
                rd(0, self.height-1)
            ) 
            # Да, я знаю что рандомная генерация без учета свободных клеток крайне тупа и неэффективна, 
            # но чел, это тупо демка для либы которой никто не пользуется...
    
    async def refresh(self):
        await super().refresh()
        
        for pos, pixel in self._snake_parts.items():
            self._buffer.set(
                *(Vec2(*pos) + self.padding[2, 0]),
                pixel
            )
        
        self._buffer.set(
            *(self._apple_position + self.padding[2, 0]),
            self._apple_pixel
        )
        
        if self.snake_is_dead:
            self._buffer.pasteByAnchor(
                0, 0, 
                Drawer.renderTextBuffer(
                    f'{'You win!\n' if self._snake_length >= self.width * self.height else ''}Your score: {self._snake_length - self._snake_length_initial}\nPress Enter\nto restart', 
                    self._text_pixel
                ),
                Anchor.center,
                self.padding
            )
            
    async def simulation(self):
        if self.snake_is_dead:
            return
        
        match self._snake_direction:
            case 0:
                self._snake_position += (0, -1)
            case 1:
                self._snake_position += (-1, 0)
            case 2:
                self._snake_position += (0, 1)
            case 3:
                self._snake_position += (1, 0)
            case _:
                raise RuntimeError()
        
        if self._snake_position.toTuple() in self._snake_parts or \
            not (0 <= self._snake_position.x  < self.width and \
                 0 <= self._snake_position.y < self.height):
                
            self.killSnake()
            
        if self.snake_is_dead is False:
            self._snake_parts[self._snake_position.toTuple()] = self._snake_pixel
            
            if len(self._snake_parts) >= self._snake_length:
                self._snake_parts = {
                    pos: self._snake_parts[pos] 
                    for pos in tuple(self._snake_parts)[len(self._snake_parts)-self._snake_length:]
                }
            
            head_symbol = '▲'
            match self._snake_direction:
                case 1:
                    head_symbol = '◄'
                case 2:
                    head_symbol = '▼'
                case 3:
                    head_symbol = '►'
            
            self._snake_parts[tuple(self._snake_parts)[-1]] = Pixel.changePixel(
                self._snake_pixel, 
                symbol=head_symbol
            )
            for pos in tuple(self._snake_parts)[1:-1]:
                self._snake_parts[pos] = Pixel.changePixel(self._snake_pixel, symbol='■')
            self._snake_parts[tuple(self._snake_parts)[0]] = Pixel.changePixel(self._snake_pixel, symbol='•')
            
            if self._snake_position == self._apple_position:
                self._snake_length += 1
                self.createApple()
        
        self.setFlagRefresh()
    
    def killSnake(self):
        self._snake_is_dead = True
        
        last_part_pos = tuple(self._snake_parts.keys())[-1]
        self._snake_parts[last_part_pos] = Pixel.changePixel(
            self._snake_parts[last_part_pos], symbol='X'
        )
    
    def inputKey(self, key: str) -> bool:
        # Да, я знаю что между симуляциями можно прожать, например a w двигаясь s, но чел...
        match key.lower():
            case 'w':
                if self._snake_direction != 2:
                    self._snake_direction = 0
            case 'a':
                if self._snake_direction != 3:
                    self._snake_direction = 1
            case 's':
                if self._snake_direction != 0:
                    self._snake_direction = 2
            case 'd': 
                if self._snake_direction != 1:
                    self._snake_direction = 3
                
            case Keys.ENTER:
                if self.snake_is_dead:
                    self.reloadSnake()
                    
            case _:
                return False
        return True
    
    async def render(self) -> Buffer[Pixel]:
        if self.selected and Func.every(f'snake_timer_widget:"{self.name}"', self._snake_delay):
            await self.simulation()
        
        return await super().render()
    
    async def awaitingRefresh(self) -> bool:
        return True
    
    def getClearPixel(self):
        return self._clear_pixel
    
    @property
    def snake_is_dead(self) -> bool:
        return self._snake_is_dead

    @property
    def snake_pixel(self) -> Union[Pixel, None]:
        return self._snake_pixel
    @snake_pixel.setter
    def snake_pixel(self, value: Union[Pixel, None]):
        self._snake_pixel = value
    
    @property
    def apple_pixel(self) -> Union[Pixel, None]:
        return self._apple_pixel
    @snake_pixel.setter
    def apple_pixel(self, value: Union[Pixel, None]):
        self._apple_pixel = value
        
    @property
    def text_pixel(self) -> Union[Pixel, None]:
        return self._text_pixel
    @snake_pixel.setter
    def text_pixel(self, value: Union[Pixel, None]):
        self._text_pixel = value


Core.initialized_all_threads_event.add(
lambda: 
    WindowManager.openNewWindow(
        TitledWindow(
            title='Snake',
            title_style=1,
            size_by_objects=True,
            objects_direction=Orientation.vertical,
            widgets=[
                SnakeWidget(
                    snake_speed=2.5,
                    size=[25, 10]
                ),
                Label(
                    text='Control: wasd',
                    clear_pixel=Pixels.b_dark_gray,
                    size_hint=[1, None]
                )
            ]
        )
    )
)

if __name__ == '__main__':
    Core.init(
        change_current_directory=__file__
    )
    Core.run()
    Core.term()