from ..Classes.Event import Event
from ..Log import Log
from ..GVars import GVars
import asyncio


class BaseThread:
    _threads: dict[str, 'BaseThread'] = {}
    init_all_event: Event = Event()
    _init_all_event_called: bool = False
    
    @classmethod
    def stopAll(cls):
        for thread in cls._threads.values():
            if thread.is_enable:
                thread.stop()
    
    def __init__(self, delay: float = 0.5):
        self._init_event = Event()
        self._sim_event = Event(self.simulation)
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
                await self._sim_event.invokeAsync()
                await asyncio.sleep(self._delay)

        except asyncio.CancelledError:
            if GVars.DEBUG_SHOW_CANCELLED_THREAD_MESSAGE:
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
        if False in (thread.is_init and thread.is_term is False for thread in self.__class__._threads.values()) or \
            self.__class__._init_all_event_called is True:
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