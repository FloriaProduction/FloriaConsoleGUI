from ..Log import Log
from ..Threads import BaseThread
from ..Config import Config

class SimulationThread(BaseThread):
    def __init__(self):
        super().__init__(1/Config.SPS)
        
    
    