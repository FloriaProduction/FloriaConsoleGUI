import asyncio
import time

from ..Classes import Event, Counter
from ..Log import Log
from ..Config import Config
from .. import Func


class BaseThread:
    _threads: dict[str, 'BaseThread'] = {}
    init_all_event: Event = Event()
    _init_all_event_called: bool = False
    _amt_sim = Counter()
    
    @classmethod
    def stopAll(cls):
        for thread in tuple(cls._threads.values()):
            if thread.is_enable:
                thread.stop()
    
    def __init__(self, delay: float = 0.5):
        self._init_event = Event()
        self._sim_event = Event(self.simulation, error_ignored=False)
        self._term_event = Event(self.termination)
        self._inited = False
        self._termed = False
        self._enabled = True
        self._delay = delay
        
        self.__class__._threads[self.name] = self
        
    async def run(self):
        try:
            await self._init_event.invokeAsync()
            self._inited = True
            Log.writeOk(f'initialized', self)
                        
            self._checkAllInitialized()
                        
            while self._enabled:
                # t1 = time.perf_counter()
                
                if Func.every(f'_sps_{self.name}', self.delay, True):
                    await self._sim_event.invokeAsync()
                    self.__class__._amt_sim.add(self.name)
                
                # sleep_time = self.delay - (time.perf_counter()-t1)
                
                await asyncio.sleep(
                    0
                    # max(
                    #     sleep_time, 
                    #     0
                    # )
                )

        except asyncio.CancelledError:
            if Config.DEBUG_SHOW_CANCELLED_THREAD_MESSAGE:
                Log.writeNotice('cancelled', self)
            
        except:
            Log.writeError(self)
            BaseThread.stopAll()
            
        finally:
            await self._term_event.invokeAsync()
            self._termed = True
            Log.writeOk(f'terminated', self)
            
            self.__class__._threads.pop(self.name)
    
    def _checkAllInitialized(self):
        if self.__class__._init_all_event_called is True or \
            False in (thread.is_init and thread.is_term is False for thread in self.__class__._threads.values()):
            return
        
        self.__class__.init_all_event.invoke()
        self.__class__._init_all_event_called = True
        
        Log.writeOk(f'all threads initialized', self)
        
    def __str__(self):
        return f'{self.__class__.__name__}'
    
    def stop(self):
        self._enabled = False
    
    async def simulation(self):
        pass
    async def termination(self):
        pass
    
    @property
    def name(self) -> str:
        return self.__class__.__name__
    @property
    def is_init(self) -> bool:
        return self._inited
    @property
    def is_term(self) -> bool:
        return self._termed
    @property
    def is_enable(self) -> bool:
        return self._enabled
    @property
    def delay(self) -> float:
        return self._delay
    @delay.setter
    def delay(self, value: float):
        self._delay = value
    @property
    def init_event(self) -> Event:
        return self._init_event
    @property
    def sim_event(self) -> Event:
        return self._sim_event
    @property
    def term_event(self) -> Event:
        return self._term_event