from typing import Union, Iterable

from ...Classes import Vec2, Vec3, Vec4, Event
from .Widget import Widget
from ..Pixel import Pixel
from ..Animation import Animation
from ...Managers.AnimationManager import AnimationManager

class Media(Widget):
    def __init__(
        self,
        size: Union[Vec2[int], Iterable[int]] = None,
        min_size: Union[Vec2[Union[int, None]], Iterable[Union[int, None]], None] = None,
        max_size: Union[Vec2[Union[int, None]], Iterable[Union[int, None]], None] = None,
        padding: Union[Vec4[int], Iterable[int]] = None,
        offset_pos: Union[Vec3[int], Iterable[int]] = None, 
        clear_pixel: Union[Pixel, tuple[Union[Vec3[int], Iterable[int]], Union[Vec3[int], Iterable[int]], str], str] = None,
        name: Union[str, None] = None,
        animation: Animation = None,
        can_be_moved: bool = True,
        *args, **kwargs
        ):
        
        self._animation: Animation = animation if isinstance(animation, Animation) else AnimationManager.get(animation)
        
        super().__init__(
            size=size if size is not None else self._animation.size, 
            min_size=min_size,
            max_size=max_size,
            padding=padding, 
            offset_pos=offset_pos, 
            clear_pixel=clear_pixel, 
            name=name,
            can_be_moved=can_be_moved,
            *args, **kwargs
        )
        
        self._animation_change_event = Event()
        
    
    async def refresh(self):
        await super().refresh()
        
        if self.animation is None:
            return
        
        self._buffer.paste(
            self.padding.left,
            self.padding.top,
            self.animation.render().resize(*self.size)
        )
    
    async def awaitingRefresh(self):
        return self.animation.is_next
    
    async def render(self):
        if self.animation.is_next:
            self.setFlagRefresh()
        
        return await super().render()
    
    def getAnimation(self) -> Animation:
        return self._animation
    def setAnimation(self, value: Union[Animation, None]):
        self._animation = value
        self._animation_change_event.invoke()
        self.setFlagRefresh()
    
    @property
    def animation(self) -> Animation:
        return self.getAnimation()
    @animation.setter
    def animation(self, value: Union[Animation, None]):
        self.setAnimation(value)
    
    @property
    def animation_change_event(self) -> Event:
        return self._animation_change_event
    
        