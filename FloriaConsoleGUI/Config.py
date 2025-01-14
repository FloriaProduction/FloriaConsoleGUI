import asyncio

class Config:
    ASYNC_EVENT_LOOP = asyncio.get_event_loop()
    
    SPS = 30
    FPS = 30
    
    CLEAR_LINES = 30
    
    # Core
    CORE_MODIFY_WIN_REGEDIT = True
    CORE_WRITE_WARNING_DYNAMIC_MODULE = True

    # Parser
    PARSER_SKIP_UNKNOWED_ANNOTATIONS = True
    
    # Drawer
    DRAWER_MAX_SIZE_CACHE = 5
    
    # Debug
    DEBUG_SHOW_INPUT_KEY = False
    DEBUG_SHOW_CANCELLED_THREAD_MESSAGE = False
    DEBUG_SHOW_ANSIICOLOR_CHARS = False
    DEBUG_SHOW_DEBUG_DATA = False  
    
    debug_data = {}
