import asyncio

class GVars:
    ASYNC_EVENT_LOOP = asyncio.get_event_loop()
    
    SPS = 30
    FPS = 15
    
    CLEAR_LINES = 30
        
    DRAWER_MAX_SIZE_CACHE = 5
    
    WRITE_WARNING_DYNAMIC_MODULE = True
    PARSER_SKIP_UNKNOWED_ANNOTATIONS = True
    
    DEBUG_SHOW_INPUT_KEY = False
    DEBUG_SHOW_CANCELLED_THREAD_MESSAGE = False
    DEBUG_SHOW_ANSIICOLOR_CHARS = False
    
