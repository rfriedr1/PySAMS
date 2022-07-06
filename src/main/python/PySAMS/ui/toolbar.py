"""
This is the toolbar that is shown in the Apps MainWindow

Toolbar inherits from PyQT Toolbar and adds new stuff to it
"""

from config.logging_conf import logger
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# set logger name to the name of the module
logger.name = __name__


class MyToolBar(QToolBar):
    """
    generate a custom toolbar for the PySAMS main window

    MyToolBar inherits from the QToolbar

    Returns:
        None
    """

    def __init__(self, *args):
        QToolBar.__init__(self, *args)

        # set orientation of the toolbar
        #self.setOrientation(QtCore.Qt.Vertical)

        # toolbar is not movable by user
        self.setMovable(False)

        # set toolbar area
        # this doesnt work since the MainMenu is managing the toolbar
        # toolbar area can be set when addToolbar(area, tollbar-object)
        # self.setAllowedAreas(QtCore.Qt.LeftToolBarArea)

        # set button style = 3 (icon and text)
        self.setToolButtonStyle(3)

        # add actions which will add buttons
        self.userprojectsPageAction = QAction(QIcon('exit.png'), "Dashboard", self)
        self.addAction(self.userprojectsPageAction)

        self.projectsPageAction = QAction(QIcon('exit.png'), "Users/Projects", self)
        self.addAction(self.projectsPageAction)

        self.samplesPageAction = QAction(QIcon('exit.png'), "Samples")
        self.addAction(self.samplesPageAction)

        self.prepPageAction = QAction(QIcon('exit.png'), "Prep")
        self.addAction(self.prepPageAction)

        self.graphPageAction = QAction(QIcon('exit.png'), "Graph")
        self.addAction(self.graphPageAction)
