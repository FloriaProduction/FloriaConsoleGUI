from FloriaConsoleGUI import *
from FloriaConsoleGUI.Managers import *


@Core.init_all_event.dec
def init():
    Core.addDynamicModule('./dyn.py', 'dyn')
    Parser.setFile('./dyn.json')

@Core.SimulationThread.sim_event.dec
def sim():
    Core.checkDynamicModules()
    Parser.checkUpdate()

if __name__ == "__main__":
    Core.init()
    Core.start()
    Core.term()