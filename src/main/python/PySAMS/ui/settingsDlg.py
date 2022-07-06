"""
This is the UI that displays the Settings Window
"""

from config.logging_conf import logger
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import config.config as config

# set logger name to the name of the module
logger.name = __name__


class MySettingsDlg(QtWidgets.QDialog):
    """
    create a dialog that displays all the settings

    A tabbed dialog window is being created and depending
    on the selection in the list widget the associated tab
    is displayed

    Returns:
        None
    """

    def __init__(self, *args):
        logger.debug('MySettingsDialog -- create MySettingsDialog')
        super(MySettingsDlg, self).__init__(*args)
        self.setWindowTitle('Settings')

        # === bild full layout ===
        # == left column ==
        # add a label
        self.label = QtWidgets.QLabel('Settings', self)
        # add a list widget
        self.listBoxItems = ['database', 'paths']
        self.listBox = QtWidgets.QListWidget(self)
        self.listBox.addItems(self.listBoxItems)
        self.listBox.itemSelectionChanged.connect(self.list_on_change)
        # add OK and Cancel buttons
        self.buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, QtCore.Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        # == right column ==
        # tab widget
        self.tabs = QtWidgets.QTabWidget()
        self.tab1 = QtWidgets.QWidget()
        self.tab2 = QtWidgets.QWidget()
        # tab widget: add tabs to tab-widget
        self.tabs.addTab(self.tab1, "database")
        self.tabs.addTab(self.tab2, "paths")
        # tab widget: create tab1 layout (Database)
        self.tab1layout = QtWidgets.QFormLayout()
        self.dbHostLineEdit = QtWidgets.QLineEdit()
        self.tab1layout.addRow("Host", self.dbHostLineEdit)
        self.dbUserLineEdit = QtWidgets.QLineEdit()
        self.tab1layout.addRow("User", self.dbUserLineEdit)
        self.dbnameLineEdit = QtWidgets.QLineEdit()
        self.tab1layout.addRow("Database", self.dbnameLineEdit)
        self.dbpasswdLineEdit = QtWidgets.QLineEdit()
        self.dbpasswdLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.tab1layout.addRow("Password", self.dbpasswdLineEdit)
        self.tab1.setLayout(self.tab1layout)
        # tab widget: create tab2 layout (paths)
        self.tab2layout = QtWidgets.QFormLayout()
        self.tab2layout.addRow("path to images on server", QtWidgets.QLineEdit())
        self.tab2layout.addRow("path to reports on server", QtWidgets.QLineEdit())
        self.tab2layout.addRow("path to input files on server", QtWidgets.QLineEdit())
        self.tab2layout.addRow("path to reports on local PC", QtWidgets.QLineEdit())
        self.tab2layout.addRow("path to report templates", QtWidgets.QLineEdit())
        self.tab2.setLayout(self.tab2layout)

        # == combine elements into the window layout ==
        self.vlayout = QtWidgets.QVBoxLayout()
        self.vlayout.setContentsMargins(0, 10, 0, 0)
        self.vlayout.addWidget(self.label)
        self.vlayout.addWidget(self.listBox)
        self.vlayout.addWidget(self.buttons)
        #
        self.hlayout = QtWidgets.QHBoxLayout()
        self.hlayout.addLayout(self.vlayout)
        self.hlayout.addWidget(self.tabs)
        #
        self.setLayout(self.hlayout)

        # first the database section is selected in the ListWidget
        # so load those settings
        self.listBox.setCurrentRow(0)
        self.tabs.setCurrentIndex(0)
        self.readSettings('database')

        # actually show the UI
        logger.debug('MySettingsDialog -- execute dialog')
        self.exec()

    def readSettings(self, section):
        """
        read the settings from the wanted section of the ini file

        then read the settings and display in the fields

        Args:
            section: string of the section name in the config file to be loaded

        Returns:
            None
        """
        logger.debug('MySettingsDialog -- readSetting of section: ' + section)
        # get the myconfig object instance that is instantiated in the config.py
        # don't intantiate again to create a new object
        logger.debug('MySettingsDialog -- call the myconfig instannce')
        myconfig = config.myconfig

        # load the values from the config file under the selected section
        # and display in the associated indicators
        if section == 'database':
            logger.debug('MySettingsDialog -- read values under section: ' + section)

            s = myconfig.get(section, 'dbhost')
            logger.debug('MySettingsDialog -- read value "dbhost": ' + s)
            self.dbHostLineEdit.setText(s)

            s = myconfig.get(section, 'dbuser')
            logger.debug('MySettingsDialog -- read value "dbuser": ' + s)
            self.dbUserLineEdit.setText(s)

            s = myconfig.get(section, 'dbname')
            logger.debug('MySettingsDialog -- read value "dbname": ' + s)
            self.dbnameLineEdit.setText(s)

            s = myconfig.get(section, 'dbpasswd')
            logger.debug('MySettingsDialog -- read value "dbpasswd": xxx')
            self.dbpasswdLineEdit.setText(s)

        elif section == 'paths':
            logger.debug('MySettingsDialog -- read values under section: ' + section)

            s = myconfig.get(section, 'path_to_reports_on_server')
            logger.debug('MySettingsDialog -- read value "path_to_reports_on_server": ' + s)

    # pyqt slots for handling the events
    @QtCore.pyqtSlot()
    def list_on_change(self):
        # selection in the list on the left side was changed
        # change tabs accordingly and perform actions
        logger.debug('MySettingsDialog -- run "list_on_change" ')
        sender = self.sender()
        # print(str(sender.currentRow()))
        if sender.currentRow() == 0:
            self.tabs.setCurrentIndex(0)
            self.readSettings('database')
        elif sender.currentRow() == 1:
            self.tabs.setCurrentIndex(1)
            self.readSettings('paths')
