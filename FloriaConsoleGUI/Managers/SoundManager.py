import os
import playsound

from ..Log import Log
from .. import Func


class SoundManager:
    # name: path
    _sounds: dict[str, str] = {}

    @classmethod
    def register(cls, name: str, path: str, rewrite: bool = False):
        if not os.path.exists(path):
            raise ValueError(
                f'File "{path}" not found'
            )
        
        if name in cls._sounds and not rewrite:
            Log.writeWarning(f'Sound "{name}" already registered', cls)
            return
            
        cls._sounds[name] = path
        
    @classmethod
    def play(cls, name: str):
        try:
            playsound.playsound(cls._sounds[name], False)
        except:
            Log.writeError(cls)
    
    @classmethod
    def load(cls, path: str):
        '''
            Path to a json file with data like:\n
            [
                {
                    name: `str` - sound name,
                    path: `str` - path to file,
                }, \n
                ...
            ]
        '''
        dir_path = os.path.dirname(path)
        
        sounds_data: list[dict[str, any]] = Func.readJson(path)
        for data in sounds_data:            
            cls.register(
                data['name'],
                f'./{dir_path}/{data['path']}'
            )
