from typing import Union, Iterable
import time
import math

from ..Classes import Vec2, Buffer, Event
from ..Graphic.Pixel import Pixel


class Animation:
    def __init__(
        self, 
        name: str,
        loop: bool = True,
        frames: Union[Iterable[Buffer[Pixel]], Buffer[Pixel]] = (),
        delay: float = 1,
        *args, **kwargs
    ):
        self._name = name
        
        if isinstance(frames, Iterable):
            if len(frames) == 0:
                raise ValueError()
            self._frames: tuple[Buffer[Pixel]] = tuple(frames)
        else:
            self._frames: tuple[Buffer[Pixel]] = (frames)
        
        self._loop = loop
        self._current_frame = 0
        self._delay = delay
        
        self._time = time.perf_counter()
        
        self._end_animation_event = Event()
        

    def render(self) -> Buffer[Pixel]:
        match len(self._frames):
            case 0:
                raise
            case 1:
                return self._frames[0]
            case _:
                if self.loop is False and self.current_frame == len(self._frames) - 1:
                    return self._frames[-1]
                
                if self.is_next:
                    # высчитывает количество "прошедших" кадров
                    self._current_frame += math.floor((time.perf_counter() - self._time)/self.delay)
                    self._time = time.perf_counter()
                    
                    
                    while self._current_frame >= len(self._frames):
                        self._current_frame -= len(self._frames)
                        self._end_animation_event.invoke()
                        
                return self._frames[self.current_frame]

    @property
    def size(self) -> Vec2:
        return self._frames[0].size
    @property
    def width(self) -> int:
        return self.size.width
    @property
    def height(self) -> int:
        return self.size.height
    
    @property
    def is_next(self) -> bool:
        return self._time + self.delay <= time.perf_counter()
    
    @property
    def current_frame(self) -> int:
        return self._current_frame
    
    @property
    def loop(self) -> bool:
        return self._loop
    
    @property
    def delay(self) -> float:
        return self._delay
    @delay.setter
    def delay(self, value: float):
        self._delay = value
        
    @property
    def name(self) -> str:
        return self._name
    
    def __len__(self) -> int:
        return len(self._frames)

    def copy(self) -> 'Animation':
        return Animation(
            self.name,
            self.loop,
            self._frames,
            self.delay
        )