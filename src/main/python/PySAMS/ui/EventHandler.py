#from PyQt5.QtCore import pyqtSlot
from config.logging_conf import logger

# set logger name to the name of the module
logger.name = __name__

class EventHandler():
    """
    DOESNT SEEM TO WORK

    this is the main event handler that deals with all the
    events when a button is pressed or a list is selected
    """

    def __init__(self):
        None

    #@pyqtSlot()
    def list_on_click(self):
        print('test')

    #@pyqtSlot()
    def btn_on_click(self):
        print('PyQt5 button click')
