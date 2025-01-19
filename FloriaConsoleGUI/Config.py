import asyncio

class Config:
    ASYNC_EVENT_LOOP = asyncio.get_event_loop()
    
    SPS = 0
    FPS = 0
    
    CLEAR_LINES = 45
    
    NEW_LINE_SYMBOL = ' '
    
    
    # Core
    CORE_MODIFY_WIN_REGEDIT = True
    CORE_WRITE_WARNING_DYNAMIC_MODULE = True
    
    # Log
    LOG_ERROR_DELAY = 2
    LOG_WARNING_DELAY = 1

    # Parser
    PARSER_SKIP_UNKNOWED_ANNOTATIONS = True
    
    TAB_LENGTH = 4
    
    # Drawer
    DRAWER_MAX_SIZE_CACHE = 5
    
    # Pixel
    PIXEL_COLOR_LIMIT = False
    PIXEL_RED_DEPTH = 16
    PIXEL_GREEN_DEPTH = 16
    PIXEL_BLUE_DEPTH = 16
    
    # Debug
    DEBUG_SHOW_INPUT_KEY = False
    DEBUG_SHOW_CANCELLED_THREAD_MESSAGE = False
    DEBUG_SHOW_ANSIICOLOR_CHARS = False
    DEBUG_SHOW_DEBUG_DATA = False  
    
    debug_data = {}
