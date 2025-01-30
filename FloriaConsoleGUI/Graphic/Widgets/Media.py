from typing import Union, Iterable, overload

from .Widget import Widget
from ..Pixel import Pixel
from ...Classes import *
from ..Animation import Animation


class Media(Widget):
    @overload
    def __init__(
        self,
        size: Iterable[int] = None,
        min_size: Union[Iterable[Union[int, None]], None] = None,
        max_size: Union[Iterable[Union[int, None]], None] = None,
        size_hint: Union[Iterable[Union[float, None]], None] = None,
        padding: Union[Iterable[int]] = None,
        offset_pos: Union[Iterable[int]] = None, 
        pos_hint: Union[Iterable[Union[int, None]], None] = None,
        clear_pixel: Union[Pixel, tuple[Iterable[int], Iterable[int], str], str] = None,
        name: Union[str, None] = None,
        animation: Animation = None,
        size_by_animation: bool = True,
        **kwargs
    ): ...
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.__animation_change_event = Event()
        
        self._size_by_animation = kwargs.get('size_by_animation', True)
        self._animation: Union[Animation, None] = None
        self.setAnimation(
            kwargs.get('animation')
        )

    async def refresh(self):
        await super().refresh()
        
        if self.animation is not None:
            self._buffer.paste(
                0, 0,
                self.animation.render().resize(
                    *self.size
                )
            )

    async def awaitingRefresh(self):
        on_refresh = False if self.animation is None else self.animation.is_next
        if on_refresh:
            self.setFlagRefresh()
        
        return on_refresh
    
    def getAnimation(self) -> Union[Animation, None]:
        return self._animation
    def setAnimation(self, animation: Union[Animation, None]):
        self._animation = animation
        if self.size_by_animation and self._animation is not None:
            self.size = self._animation.size
        self.animation_change_event.invoke()
        self.setFlagRefresh()
    @property
    def animation(self) -> Union[Animation, None]:
        return self.getAnimation()
    @animation.setter
    def animation(self, value: Union[Animation, None]):
        self.setAnimation(value)
    
    @property
    def size_by_animation(self) -> bool:
        return self._size_by_animation
    @size_by_animation.setter
    def size_by_animation(self, value: bool):
        self._size_by_animation = value
    
    @property
    def animation_change_event(self) -> Event:
        return self.__animation_change_event
    