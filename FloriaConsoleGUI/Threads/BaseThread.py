import asyncio

from ..Classes import Event, Counter
from ..Log import Log
from ..Config import Config
from .. import Func


class BaseThread:
    _threads: dict[str, 'BaseThread'] = {}
    init_all_event: Event = Event()
    _init_all_event_called: bool = False
    _amount_simulation = Counter()
    
    @classmethod
    def stopAll(cls):
        for thread in tuple(cls._threads.values()):
            if thread.is_enable:
                thread.stop()
    
    def __init__(self, delay: float = 0.5):
        self._init_event = Event(self.initialization)
        self._sim_event = Event(self.simulation, error_ignored=True, await_input=True)
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
                if Func.every(f'_sps_{self.name}', self.delay, True):
                    await self._sim_event.invokeAsync()
                    self.__class__._amount_simulation.add(self.name)
                await asyncio.sleep(0)

        except asyncio.CancelledError:
            if Config.DEBUG_SHOW_CANCELLED_THREAD_MESSAGE:
                Log.writeNotice('cancelled', self)
            
        except:
            Log.writeError(self)
            input('Press to continue...')
            BaseThread.stopAll()
            
        finally:
            await self._term_event.invokeAsync()
            self._termed = True
            Log.writeOk(f'terminated', self)
            
            self.__class__._threads.pop(self.name)
    
    def _checkAllInitialized(self):
        if self.__class__._init_all_event_called is True or \
            False in (thread.is_initialized and thread.is_terminated is False for thread in self.__class__._threads.values()):
            return
        
        self.__class__.init_all_event.invoke()
        self.__class__._init_all_event_called = True
        
        Log.writeOk(f'all threads initialized', self)
        
    def stop(self):
        self._enabled = False
    
    async def initialization(self):
        pass
    async def simulation(self):
        pass
    async def termination(self):
        pass
    
    @property
    def name(self) -> str:
        return self.__class__.__name__
    @property
    def is_initialized(self) -> bool:
        return self._inited
    @property
    def is_terminated(self) -> bool:
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
    def initialized_event(self) -> Event:
        return self._init_event
    @property
    def simulation_event(self) -> Event:
        return self._sim_event
    @property
    def terminated_event(self) -> Event:
        return self._term_event
    
    def __str__(self):
        return f'{self.__class__.__name__}'