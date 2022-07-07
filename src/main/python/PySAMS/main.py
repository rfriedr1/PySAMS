"""
Main App of the PySAMS
"""

import sys
import time

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QMainWindow
from ui.menubar import MyMenuBar
from ui.toolbar import MyToolBar
from ui.SplashScreen import MySplashScreen
# from database import pysamsdb
from database.pysamsdb import *  # this is the already instantiated MyDatabase object connecting the the AMS DB
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
from config.config import myconfig
from config.logging_conf import logger

__version__ = '2022-July-06'
__author__ = 'Ronny Friedrich'

# set logger name to the name of the module
logger.name = __name__


class PySAMS(QMainWindow):
    """
    main class for the PySAMS App.

    this is the main class of the PySAMS App.
    It is intended to generate plots of various QC or
    statistical data directly retrieved from a database.

    Returns:
        None
    """

    def __init__(self):
        """
        Initialize the PySAMS main window object.
        Create all the windows elements (buttons etc etc) of the main window
        """
        super().__init__()  # method calls are directed to the parent

        splash.showMessage(splash.message() + '\n' + 'loading app data', QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom,
                           QtCore.Qt.white)

        # log system info
        logger.debug('system version: Python ' + sys.version)
        logger.debug('system platform: ' + sys.platform)

        # =======================================================================
        # set basic window settings such as size an titel etc
        logger.debug('initialize main app')
        # splash.showMessage(splash.message() + '\n' + 'set main window parameters',
        #                    QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom, QtCore.Qt.white)
        self.title = 'PySAMS v.' + str(__version__)
        logger.debug(self.title)
        self.left = 30
        self.top = 30
        self.width = 800
        self.height = 600
        # create window
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # =======================================================================
        # initialize event handler for button clicks and so on
        # eventhandler = EventHandler()

        # =======================================================================
        # create menubar
        self.create_menu_bar()

        # =======================================================================
        # add a custom toolbar
        self.create_tool_bar()

        # =======================================================================
        # add a status bar
        self.create_status_bar()

        # =======================================================================
        # read config file and load settings
        self.read_config()

        # =======================================================================
        # connect to database and load some data
        logger.info('establishing first database connection')
        splash.showMessage(splash.message() + '\n' + 'establishing database connection',
                           QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom, QtCore.Qt.white)
        appctxt.app.processEvents()

        # self.db = pysamsdb.MyDatabase()
        # mydb = MyDatabase()
        # mydb = pysamsdb.mydb
        # retrieve DB Version
        db_vers = str(mydb.get_dbversion())
        splash.showMessage(splash.message() + '\n' + 'found database version: ' + db_vers,
                           QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom, QtCore.Qt.white)
        appctxt.app.processEvents()

        # =======================================================================
        # create a tab widget that will be the central widget of the window
        logger.debug('initialize main tab widget')
        main_tabwidget = QtWidgets.QTabWidget()
        main_tabwidget.setTabShape(0)
        self.create_dashboard_tab(main_tabwidget)  # create and add the Dashboard tab to the main tab widget
        self.create_user_project_info_tab(main_tabwidget)  # create and add the User-Info/Project-Info tab to the main tab widget
        self.create_sample_info_tab(main_tabwidget)  # create and add the Sample-Info tab to the main tab widget
        # set the tab widget to be the central widget of the window
        self.setCentralWidget(main_tabwidget)

        # =======================================================================
        # actually show the UI
        # as soon as the UI shows, the splash screen closes
        # therefore do all the stuff like loading prefs etc before showing the UI
        logger.debug('showing UI')
        self.show()

    # =======================================================================
    def create_tool_bar(self):
        """
        Generate a tool bar

        Args:
            None

        Returns:
            None
        """
        logger.debug('initialize toolbar bar')
        # splash.showMessage(splash.message() + '\n' + 'create toolbar..',
        #                    QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom, QtCore.Qt.white)
        self.toolbar = MyToolBar()
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolbar)

    # =======================================================================
    def create_menu_bar(self):
        """
        Generate a menu bar

        Args:
            None

        Returns:
            None
        """
        # =======================================================================
        # create MenuBar from my custom menubar class
        logger.debug('initialize menu bar')
        # splash.showMessage(splash.message() + '\n' + 'Create Menubar...',
        #                    QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom, QtCore.Qt.white)
        menubar = MyMenuBar(self)
        self.setMenuBar(menubar)

    # =======================================================================
    def create_status_bar(self):
        """
        Generate a status bar

        Args:
            None

        Returns:
            None
        """
        # =======================================================================
        # create statusbar
        # splash.showMessage(splash.message() + '\n' + 'create statusbar..',
        #                    QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom, QtCore.Qt.white)
        logger.debug('initialize status bar')
        self.statusbar = QtWidgets.QStatusBar()  # create a statusbar
        self.setStatusBar(self.statusbar)  # assign statusbar to the MainWindow
        self.statusbar.showMessage('PySAMS', 2000)

    # =======================================================================
    def read_config(self):
        """
        read config file and load settings

        Args:
            None

        Returns:
            None
        """
        logger.info('loading config data')
        splash.showMessage(splash.message() + '\n' + 'loading config data...',
                           QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom, QtCore.Qt.white)
        appctxt.app.processEvents()
        
        # get configuration-file object from the config.py file
        logger.debug('get config object')
        # myconfig = config.myconfig  # config.myconfig is a variable that already has the MyConfig Object
        logger.debug('check whether config data are present')
        if myconfig.checkconfig():
            logger.debug('checkconfig = True')
            splash.showMessage(splash.message() + '\n' + 'config data are present',
                               QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom, QtCore.Qt.white)
            appctxt.app.processEvents()
        else:
            logger.debug('checkconfig = False')
            splash.showMessage(splash.message() + '\n' + 'config data are missing, writing default',
                               QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom, QtCore.Qt.white)
            appctxt.app.processEvents()

    # =======================================================================
    def create_dashboard_tab(self, parent: QtWidgets.QTabWidget):
        """
        Generate the Dashboard tab of the main Tab Widget

        Args:
            parent: is the main tab widget where this tab goes to

        Returns:
            None
        """
        # TODO Finish building the Dashboard Tab
        logger.debug('create_dashboard_tab - initialize Dashboard Tab')
        # create a new tab for the dashboard
        tab_dashboard = QtWidgets.QTabWidget()
        tab_dashboard.setToolTip('Dashboard tab')
        # add the tab to the parent tabwidget
        parent.addTab(tab_dashboard, 'Dashboard')

        # create fields to display info on the dashboard
        textzoom = 20  # increase text size by this for textedits

        # query DB here for values to be displayed for the first time
        label_count_oxas = QtWidgets.QLabel('number of oxas')
        textedit_count_oxas = QtWidgets.QTextEdit(mydb.get_number_available_oxas())
        textedit_count_oxas.setReadOnly(True)
        textedit_count_oxas.setAlignment(QtCore.Qt.AlignCenter)
        textedit_count_oxas.zoomIn(textzoom)
        textedit_count_oxas.setFrameShape(QtWidgets.QFrame.NoFrame)
        # textedit_count_oxas.setFrameShadow(QtWidgets.QFrame.Plain)

        label_count_blanks = QtWidgets.QLabel('number of blanks')
        textedit_count_blanks = QtWidgets.QTextEdit(mydb.get_number_available_blanks())
        textedit_count_blanks.setReadOnly(True)
        textedit_count_blanks.setAlignment(QtCore.Qt.AlignCenter)
        textedit_count_blanks.zoomIn(textzoom)
        textedit_count_blanks.setFrameShape(QtWidgets.QFrame.NoFrame)

        label_unprepped_samples = QtWidgets.QLabel('ready for prep')
        textedit_unprepped_samples = QtWidgets.QTextEdit(mydb.get_number_of_unprepped_samples())
        textedit_unprepped_samples.setReadOnly(True)
        textedit_unprepped_samples.setAlignment(QtCore.Qt.AlignCenter)
        textedit_unprepped_samples.zoomIn(textzoom)
        textedit_unprepped_samples.setFrameShape(QtWidgets.QFrame.NoFrame)

        label_count_samples_for_graph = QtWidgets.QLabel('ready for graph')
        textedit_count_samples_for_graph = QtWidgets.QTextEdit(mydb.get_number_of_samples_ready_for_graph())
        textedit_count_samples_for_graph.setReadOnly(True)
        textedit_count_samples_for_graph.setAlignment(QtCore.Qt.AlignCenter)
        textedit_count_samples_for_graph.zoomIn(textzoom)
        textedit_count_samples_for_graph.setFrameShape(QtWidgets.QFrame.NoFrame)

        label_count_samples_for_analysis = QtWidgets.QLabel('ready for AMS')
        textedit_count_samples_for_analysis = QtWidgets.QTextEdit(mydb.get_number_of_samples_ready_for_analysis())
        textedit_count_samples_for_analysis.setReadOnly(True)
        textedit_count_samples_for_analysis.setAlignment(QtCore.Qt.AlignCenter)
        textedit_count_samples_for_analysis.zoomIn(textzoom)
        textedit_count_samples_for_analysis.setFrameShape(QtWidgets.QFrame.NoFrame)

        label_count_samples_express = QtWidgets.QLabel('number of express')
        textedit_count_samples_express = QtWidgets.QTextEdit(mydb.get_number_of_samples_express())
        textedit_count_samples_express.setReadOnly(True)
        textedit_count_samples_express.setAlignment(QtCore.Qt.AlignCenter)
        textedit_count_samples_express.zoomIn(textzoom)
        textedit_count_samples_express.setFrameShape(QtWidgets.QFrame.NoFrame)

        # create the boxlayout
        layout = QtWidgets.QGridLayout()
        # add widgets to layout by giving the column and row numbers, no colspan or rowspan
        # layout.addWidget(label_count_oxas, 0, 0, 1, 1) # row, col, rowspan, colspan
        # column 0
        layout.addWidget(label_count_oxas, 0, 0)  # row, col
        layout.addWidget(textedit_count_oxas, 1, 0)  # row, col
        layout.addWidget(label_count_blanks, 2, 0)  # row, col
        layout.addWidget(textedit_count_blanks, 3, 0)  # row, col
        # column 1
        layout.addWidget(label_unprepped_samples, 0, 1)
        layout.addWidget(textedit_unprepped_samples, 1, 1)
        layout.addWidget(label_count_samples_for_graph, 2, 1)
        layout.addWidget(textedit_count_samples_for_graph, 3, 1)
        layout.addWidget(label_count_samples_for_analysis, 4, 1)
        layout.addWidget(textedit_count_samples_for_analysis, 5, 1)
        # column 2
        layout.addWidget(label_count_samples_express, 0, 2)
        layout.addWidget(textedit_count_samples_express, 1, 2)

        tab_dashboard.setLayout(layout)

    # =======================================================================
    def create_user_project_info_tab(self, parent: QtWidgets.QTabWidget):
        """
        Generate the UserInfo/ProjectInfo tab of the main Tab Widget
        That Tab shows all info about a user and it's project
        It also gives an overview over all samples that belong to a project.

        Args:
            parent: is the main tab widget where this tab goes to

        Returns:
            None

        """
        # TODO Finish building the UserProject Tab
        logger.debug('create_UserProject_tab - initialize UserProject Tab')
        tab_userprojects = QtWidgets.QTabWidget()
        tab_userprojects.setToolTip('Information about Users and Projects')
        parent.addTab(tab_userprojects, 'User/Project Info')
        # == left column ==
        # label
        label_users = QtWidgets.QLabel('Users', self)
        # TableView of the users in the DB
        usertable = QtWidgets.QTableView()

        # treeView of the Projects and Samples
        label_projects = QtWidgets.QLabel('Projects and Samples', self)
        project_tree = QtWidgets.QTreeView()

        # query database
        """
        db = amsDBConnection()
        db.queryDB("SELECT * FROM user_t")
        for i in range(0, 11):
            logger.debug('QT Path Location ' + str(i) + ' :' + QtCore.QLibraryInfo.location(i))
        """

        # model = Tree
        # projectTree.setModel()
        # == right column ==
        # label
        label_info = QtWidgets.QLabel('Info')
        # sample table
        sampletable = QtWidgets.QTableView()
        # button
        btn_sampleinfo = QtWidgets.QPushButton('test button', self)
        btn_sampleinfo.setToolTip('test button')
        # button.clicked.connect(lambda: self.btn_on_click())
        # build layout
        vlayout_left = QtWidgets.QVBoxLayout()
        vlayout_left.addWidget(label_users)
        vlayout_left.addWidget(usertable)
        vlayout_left.addWidget(label_projects)
        vlayout_left.addWidget(project_tree)
        #
        vlayout_right = QtWidgets.QVBoxLayout()
        vlayout_right.addWidget(label_info)
        vlayout_right.addWidget(sampletable)
        vlayout_right.addWidget(btn_sampleinfo)
        #
        tablayout = QtWidgets.QHBoxLayout()
        tablayout.addLayout(vlayout_left)
        tablayout.addLayout(vlayout_right)
        tab_userprojects.setLayout(tablayout)

# =======================================================================
    def create_sample_info_tab(self, parent: QtWidgets.QTabWidget):
        """
        Generate the SampleInfo tab of the main Tab Widget
        That Tab shows all info about a sample

        Args:
            parent: is the main tab widget where this tab goes to

        Returns:
            None

        """
        # TODO Finish building the SampleInfo Tab
        logger.debug('create_SampleInfo_tab - initialize SampleInfo Tab')
        tab_sampleinfo = QtWidgets.QTabWidget()
        tab_sampleinfo.setToolTip('Information about a sample')
        parent.addTab(tab_sampleinfo, 'Sample Info')



# =======================================================================
# MAIN Routine
# =======================================================================
if __name__ == "__main__":
    
    packaging = True  # when using fbs for packing 

    if packaging == False:
        # =======================================================================
        # instantiate the PyQT App
        app = QtWidgets.QApplication(sys.argv)

        # =======================================================================
        # add splash screen
        splash = MySplashScreen()  # instantiate the splash screen, appearance is set during init of the object
        splash.show()  # display screen
        app.processEvents()
        splash.showMessage('starting app', QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom, QtCore.Qt.white)
        splash.showMessage(splash.message() + '\n' + 'Python ' + sys.version,
                        QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom, QtCore.Qt.white)
        splash.showMessage(splash.message() + '\n' + 'Platform ' + sys.platform,
                        QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom, QtCore.Qt.white)
        # time.sleep(10)

        # =======================================================================
        # create and start the application
        mainwindow = PySAMS()
        logger.debug('library paths: ' + ', '.join(app.libraryPaths()))  # log paths to libraries

        # =======================================================================
        # kill the splashscreen as soon as the main window is available
        splash.finish(mainwindow)

        # =======================================================================
        # run the App and exit when the App was closed
        sys.exit(app.exec_())
    else:
        appctxt = ApplicationContext()
        appctxt.app.setStyle('Breeze')
        
        # =======================================================================
        # add splash screen
        splash = MySplashScreen()  # instantiate the splash screen, appearance is set during init of the object
        splash.resize(500,200)
        splash.show()  # display screen
        appctxt.app.processEvents()
        splash.showMessage('starting app', QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom, QtCore.Qt.white)
        splash.showMessage(splash.message() + '\n' + 'Python ' + sys.version,
                        QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom, QtCore.Qt.white)
        splash.showMessage(splash.message() + '\n' + 'Platform ' + sys.platform,
                        QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom, QtCore.Qt.white)
        
        # =======================================================================
        # create and start the application
        main = PySAMS()
        logger.debug('library paths: ' + ', '.join(appctxt.app.libraryPaths()))  # log paths to libraries
        
        # =======================================================================
        # kill the splashscreen as soon as the main window is available
        splash.finish(main)
        
        exit_code = appctxt.app.exec_()
        sys.exit(exit_code)

