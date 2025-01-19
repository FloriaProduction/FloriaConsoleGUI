from typing import Union, Iterable
import os
import PIL
import PIL.GifImagePlugin
import PIL.Image

from ..Log import Log
from .. import Func
from ..Graphic import Animation, Pixel
from ..Classes import Buffer


class AnimationManager:
    _animations: dict[str, Animation] = {}

    @classmethod
    def get(cls, name: str) -> Animation:
        if name not in cls._animations:
            raise ValueError(
                f'Animation "{name}" not found'
            )
        return cls._animations[name].copy()
    
    @classmethod
    def register(cls, name: str, animation: Animation, rewrite: bool = False):
        if name in cls._animations and not rewrite:
            Log.writeWarning(f'Animation "{name}" already registered', cls)
            return
        
        cls._animations[name] = animation
        Log.writeOk(f'Animation "{name}" registered', cls)
    
    @classmethod
    def load(cls, path: str):
        '''
            Path to a json file with data like:\n
            [
                {
                    name: `str` - animation name,
                    path: `str` - path to img/jpeg/gif,
                    delay: `float` default=get from source file - delay between frames,
                    loop: `bool` default=True - animation is looped
                }, \n
                ...
            ]
        '''
        dir_path = os.path.dirname(path)
        
        animations_data: list[dict[str, any]] = Func.readJson(path)
        for data in animations_data:
            image = PIL.Image.open(f'./{dir_path}/{data['path']}', formats=['png', 'jpeg', 'gif'])
            
            cls.register(
                data['name'],
                Animation(
                    data['name'],
                    delay=data.get('delay', cls.getDelay(image)),
                    loop=data.get('loop', True),
                    frames=cls.getFrames(image)
                )
            )
    
    @classmethod
    def getDelay(cls, image: Union[PIL.Image.Image, PIL.GifImagePlugin.GifImageFile]) -> float:
        if isinstance(image, PIL.GifImagePlugin.GifImageFile):
            return image.info.get('duration') / 1000
        return 0
    
    @classmethod
    def getFrames(cls, image: Union[PIL.Image.Image, PIL.GifImagePlugin.GifImageFile]) -> Iterable[Buffer[Pixel]]:
        def convertImageToBuffer(image: Union[PIL.Image.Image, PIL.GifImagePlugin.GifImageFile]) -> Buffer[Pixel]:
            return Buffer(
                image.width,
                image.height,
                None,
                [
                    Pixel(back_color=pixel_data[:3]) if pixel_data[3] > 125 else None for pixel_data in image.convert('RGBA').getdata()
                ]
            )
        
        if isinstance(image, PIL.GifImagePlugin.GifImageFile):
            frames = []
            for i in range(image.n_frames):
                image.seek(i)
                frames.append(
                    convertImageToBuffer(image)
                )
            return frames
        
        else:
            return [
                Buffer(
                    image.width,
                    image.height,
                    None,
                    convertImageToBuffer(image)
                )
            ]
                
    