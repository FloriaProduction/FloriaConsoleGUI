from ..Log import Log
from ..Threads import BaseThread
from ..GVars import GVars

class SimulationThread(BaseThread):
    def __init__(self):
        super().__init__(1/GVars.SPS)
        
    
    