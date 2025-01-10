import asyncio

class GVars:
    ASYNC_EVENT_LOOP = asyncio.get_event_loop()
    
    SPS = 30
    FPS = 15
    
    CLEAR_LINES = 30
        
    DRAWER_MAX_SIZE_CACHE = 5
    
    DEBUG_SHOW_INPUT_KEY = False
    DEBUG_SHOW_CANCELLED_THREAD_MESSAGE = False
    DEBUG_SHOW_ANSIICOLOR_CHARS = False
    DEBUG_STOP_RENDER_WHEN_WITHOUT_WINDOWS = False
    
