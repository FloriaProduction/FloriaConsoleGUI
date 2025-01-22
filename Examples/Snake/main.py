from typing import Union, Iterable
from random import randint as rd

from FloriaConsoleGUI import *
from FloriaConsoleGUI.Classes import Anchor, Buffer, Vec2, Vec3, Vec4
from FloriaConsoleGUI.Classes import *
from FloriaConsoleGUI.Graphic import *
from FloriaConsoleGUI.Graphic.Pixel import Pixel
from FloriaConsoleGUI.Graphic.Widgets import *
from FloriaConsoleGUI.Graphic.Windows import *
from FloriaConsoleGUI.Managers import *


class SnakeWidget(InteractiveWidget):
    def __init__(
        self,
        snake_pixel: Pixel | tuple[Vec3[int] | Iterable[int], Vec3[int] | Iterable[int], str] | str = None, 
        snake_speed: int = 1, # number moves in second
        snake_length: int = 3,
        apple_pixel: Pixel | tuple[Vec3[int] | Iterable[int], Vec3[int] | Iterable[int], str] | str = None, 
        text_pixel: Pixel | tuple[Vec3[int] | Iterable[int], Vec3[int] | Iterable[int], str] | str = None, 
        size: Vec2[int] | Iterable[int] = None, 
        min_size: Vec2[int | None] | Iterable[int | None] | None = None,
        max_size: Vec2[int | None] | Iterable[int | None] | None = None, 
        padding: Vec4[int] | Iterable[int] = None, 
        offset_pos: Vec3[int] | Iterable[int] = None, 
        clear_pixel: Pixel | tuple[Vec3[int] | Iterable[int], Vec3[int] | Iterable[int], str] | str = None, 
        name: str = 'snake_game', 
        can_be_moved: bool = True, 
        select_clear_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str] = None,
        tabindex: Union[int, None] = None,
        *args, **kwargs
    ):
        super().__init__(
            size=size,
            min_size=min_size,
            max_size=max_size,
            padding=padding,
            offset_pos=offset_pos,
            clear_pixel=clear_pixel,
            name=name,
            can_be_moved=can_be_moved,
            select_clear_pixel=select_clear_pixel,
            tabindex=tabindex,
            *args, **kwargs
        )
        self._snake_length_initial: int = snake_length
        
        self._snake_delay = 1 / snake_speed
        self._snake_pixel = Converter.toPixel(snake_pixel, default=Pixel((0, 255, 0), None, '█'))
        self._snake_position: Vec2[int] = None
        self._snake_parts: dict[Vec2[int], Pixel] = None
        self._snake_length: int = None
        self._snake_direction: int = 0 # w a s d  -  0 1 2 3
        self._snake_is_dead: bool = False
        self.reloadSnake()
        
        self._apple_position: Vec2[int] = None
        self._apple_pixel = Converter.toPixel(apple_pixel, default=Pixel(None, [255, 0, 0], '@'))
        self.createApple()

        self._text_pixel = Converter.toPixel(text_pixel, default=Pixel([0, 0, 0], [255, 255, 255]))

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
        
        field = Buffer(
            *self.size,
            None
        )
        
        for pos, pixel in self._snake_parts.items():
            field.set(
                *pos, 
                pixel
            )
        
        field.set(
            *self._apple_position,
            self._apple_pixel
        )
        
        self._buffer.paste(
            self.padding.left, 
            self.padding.top,
            field,
            self.padding
        )
        
        if self.snake_is_dead:
            self._buffer.pasteByAnchor(
                0, 0, 
                await Drawer.renderTextBuffer(
                    f'{'You win!\n' if self._snake_length >= self.width * self.height else ''}Your score: {self._snake_length - self._snake_length_initial}\nPress Enter\nto restart', 
                    self._text_pixel
                ),
                Anchor.center,
                self.padding
            )
            
    async def simulation(self):
        if self.snake_is_dead and self.selected:
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
        if Func.every(f'snake_timer_widget:"{self.name}"', self._snake_delay):
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

@Core.initialized_all_threads_event.dec
def _():
    WindowManager.openNewWindow(
        TitledWindow(
            title='Snake',
            direction=Orientation.vertical,
            frame=True,
            widgets=[
                SnakeWidget(
                    min_size=(20, 10),
                    snake_speed=3,
                ),
                Label(
                    text='Control: wasd',
                    clear_pixel=Pixel((255, 255, 255), (25, 25, 25)),
                    min_size=(20, None)
                )
            ]
        )
    )

if __name__ == '__main__':
    Core.init()
    Core.start()
    Core.term()