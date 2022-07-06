"""
This is the menubar that is shown in the Apps MainWindow

It inherits from the PyQt's Menubar and adds new stuff
"""

from config.logging_conf import logger
from PyQt5.QtWidgets import QMenuBar, QAction, qApp, QMessageBox
from PyQt5.QtGui import QIcon
from ui.settingsDlg import MySettingsDlg
from ui.plotwindow import PlotWindow
from ui.sqlplotwindow import SqlPlotWindow

# set logger name to the name of the module
logger.name = __name__


class MyMenuBar(QMenuBar):
    """
    Create a custom menubar that is shown in the Apps MainWindow.

    MyMenuBar inherits from the PyQT MenuBar.

    Returns:
        None
    """

    def __init__(self, *args, **kwargs):
        logger.info('create MyMenuBar')
        QMenuBar.__init__(self, *args)  # initialize the QMenuBarObject which is the parent of MyMenuBar

        # create MenuBar
        self.setNativeMenuBar(False)  # for OSX so that there's no OSX style MenuBar

        # File Menu
        self.fileMenu = self.addMenu('File')
        #  File -> Settings
        self.settingsAction = QAction(QIcon('icons\gear.bmp'), 'Settings', self)
        self.settingsAction.setStatusTip('display settings window')
        self.settingsAction.triggered.connect(self.settingsDlg)
        self.fileMenu.addAction(self.settingsAction)
        #  File -> Exit
        self.exitAction = QAction(QIcon('ui\icons\gear.bmp'), 'Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(qApp.quit)
        self.fileMenu.addAction(self.exitAction)

        # Tools Menu
        self.toolsMenu = self.addMenu('Tools')
        #  Tools -> PlotWindow
        self.plotwindowAction = QAction(QIcon('icons\gear.bmp'), 'QC + Stat Plots', self)
        self.plotwindowAction.setStatusTip('plot predefined qc and stat plots')
        self.plotwindowAction.triggered.connect(self.plotWindow)
        self.toolsMenu.addAction(self.plotwindowAction)
        #  Tools -> SQLPlotWindow
        self.sqlplotwindowAction = QAction(QIcon('icons\gear.bmp'), 'SQL Plots', self)
        self.sqlplotwindowAction.setStatusTip('generate SQL plots running custom queries')
        self.sqlplotwindowAction.triggered.connect(self.sqlplotWindow)
        self.toolsMenu.addAction(self.sqlplotwindowAction)

        # Help Menu
        self.helpMenu = self.addMenu('Help')
        # Help -> About
        self.aboutAction = QAction(QIcon('exit24.png'), 'About', self)
        self.aboutAction.setStatusTip('Infos about the program')
        self.aboutAction.triggered.connect(self.aboutDlg)
        self.helpMenu.addAction(self.aboutAction)

    def aboutDlg(self):
        logger.info('Show About Message')
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText("PySAMS")
        self.msg.setInformativeText("by Ronny Friedrich")
        self.msg.setWindowTitle("About")
        self.msg.exec()

    def settingsDlg(self):
        # displays a settings window
        # by instantiating the MySettingsDlg class
        self.settingsDlg = MySettingsDlg()

    def plotWindow(self):
        self.plotWindow = PlotWindow()

    def sqlplotWindow(self):
        self.sqlplotWindow = SqlPlotWindow()




