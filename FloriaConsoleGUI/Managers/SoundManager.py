from typing import Union, Iterable
import os
import playsound
import asyncio

from ..Log import Log

class SoundManager:
    # name: path
    _sounds: dict[str, str] = {}

    @classmethod
    def registerSound(cls, name: str, path: str, rewrite: bool = False):
        if not os.path.exists(path):
            raise ValueError(f'File "path" not found')
        
        if name in cls._sounds and not rewrite:
            Log.writeWarning(f'Sound "{name}" already registered', cls)
            
        cls._sounds[name] = path
        
    @classmethod
    def play(cls, name: str):
        try:
            playsound.playsound(cls._sounds[name], False)
        except:
            Log.writeError(cls)
        
