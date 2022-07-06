from config.logging_conf import logger
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtSql as QtSql
from database.pysamsdb import mydb  # this is the already instantiated MyDatabase object to the AMS DB
import ui.plotcanvas as plotcanvas
import pandas


# set logger name to the name of the module
logger.name = __name__


class SqlPlotWindow(QtWidgets.QMainWindow):
    """
    main class for a plot window that allows to process sql queries
    and plots the results.

    Args:
        None

    Returns:
        None
    """
    def __init__(self):
        """
        Initialize the App object.

        Create a instance attribute that holds the db parameters.
        In that way the db_params are only valid for this instance of the App

        Create all the windows elements (buttons etc etc)
        """
        logger.info('create SqlPlotWindow')
        super().__init__()  # method calls are directed to the parent

        # prepare basic windows settings
        self.title = 'Sql Plot Window'
        self.left = 10
        self.top = 10
        self.width = 800
        self.height = 600

        # create window
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # initialize event handler for button clicks and so on
        # eventhandler = EventHandler()

        # create statusbar
        self.statusbar = QtWidgets.QStatusBar()  # create a statusbar
        self.setStatusBar(self.statusbar)  # assign statusbar to the MainWindow
        self.statusbar.showMessage('SQL Plot Window', 2000)

        # create the central widget that goes into the mainwindow
        self.centralWidget = QtWidgets.QWidget()

        # add a label
        self.label = QtWidgets.QLabel('SQL query', self)
        # a textbox that holds the SQL Query
        self.querybox = QtWidgets.QTextEdit()
        # add example text to the box
        self.querybox.setText('select fm, dc13 from target_v where type = "oxa2" and fm is not null')

        # create a button
        self.button = QtWidgets.QPushButton('Run', self)
        self.button.setToolTip('run the query and generate a plotplot')
        self.button.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.button.clicked.connect(lambda: self.btn_on_click(self.querybox))

        # create a table that holds the query results
        self.datatable = QtWidgets.QTableView()  # the QSqlTableModel will be set up when running the query
        self.datatable.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)

        # create a table that shows the statistics results
        self.stattable = QtWidgets.QTableView()
        self.stattable.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)

        # create a canvas for the plot
        self.canvas = plotcanvas.MyPlotCanvas(parent=self.centralWidget, width=8, height=6, dpi=100)

        # combine all into nested layouts
        # top horz
        self.hlayouttop = QtWidgets.QHBoxLayout()
        # self.hlayouttop.setContentsMargins(5, 5, 5, 5)
        self.hlayouttop.addWidget(self.querybox)
        self.hlayouttop.addWidget(self.button)
        # self.hlayouttop.addStretch()

        # label above top horz
        self.vlayouttop = QtWidgets.QVBoxLayout()
        # self.vlayout1.setContentsMargins(5, 5, 5, 5)
        self.vlayouttop.addWidget(self.label)
        self.vlayouttop.addLayout(self.hlayouttop)

        # left vertical
        self.vlayoutleft = QtWidgets.QVBoxLayout()
        self.vlayoutleft.addWidget(self.datatable)
        self.vlayoutleft.addWidget(self.stattable)

        # horz bottom
        self.hlayoutbottom = QtWidgets.QHBoxLayout()
        # self.hlayoutbottom.setContentsMargins(5, 5, 5, 5)
        self.hlayoutbottom.addLayout(self.vlayoutleft)
        self.hlayoutbottom.addWidget(self.canvas)

        self.vlayoutmain = QtWidgets.QVBoxLayout()
        # self.vlayoutmain.setContentsMargins(5, 5, 5, 5)
        self.vlayoutmain.addLayout(self.vlayouttop)
        self.vlayoutmain.addLayout(self.hlayoutbottom)

        # central widget: assign layout to central widget
        self.centralWidget.setLayout(self.vlayoutmain)
        self.setCentralWidget(self.centralWidget)

        # actually show the UI
        self.show()

    # pyqt slots for handling the events
    @QtCore.pyqtSlot()
    def btn_on_click(self, querybox):
        sender = self.sender()
        logger.debug('SQLplotwindow -- performing query')
        logger.debug(str(querybox))
        # query database and display the results as a plot and in tables
        if len(querybox.toPlainText()) > 0:  # perform query if anything is entered at all
            qrydata = mydb.querydb(querybox.toPlainText()) # Query database and connect query to a QSqlQueryModel
            datamodel = QtSql.QSqlQueryModel()  # create QueryModel Object
            datamodel.setQuery(qrydata)  # bind resulting qrydata from the databasequery to the model
            self.datatable.setModel(datamodel) # bind datatable to the datamodel
            logger.debug('query columns ' + str(datamodel.columnCount()))
            logger.debug('query rows ' + str(datamodel.rowCount()))
            # send data to canvas
            dataframe = self.datamodel_to_dataframe(datamodel)
            self.canvas.create_plot(dataframe)
            # do some statistics of the data and show in the stattable
            self.update_stattable(dataframe)

    def datamodel_to_dataframe(self, datamodel: QtSql.QSqlQueryModel) -> pandas.DataFrame:
        """
        get the first two columns out of the datamodel into a dataframe.

        Args:
            datamodel: data from the SQLQuery also shown in the tableView

        Returns:
            dataframe:

        """
        col1label = datamodel.record(0).fieldName(0)
        col2label = datamodel.record(0).fieldName(1)
        dataframe = pandas.DataFrame()
        col1data = []
        col2data = []
        if not datamodel.record().isEmpty():
            for i in range(0, datamodel.rowCount()):
                col1data.append(datamodel.record(i).value(col1label))
                col2data.append(datamodel.record(i).value(col2label))
            # convert list into a pandas series
            list1 = pandas.Series(col1data)
            list2 = pandas.Series(col2data)
            # add series to a dataframe
            dataframe.insert(loc=0, column=col1label, value=col1data, allow_duplicates=True)
            dataframe.insert(loc=1, column=col2label, value=col2data, allow_duplicates=True)
        return dataframe

    def update_stattable(self, dataframe: pandas.DataFrame):
        """
        update the stattabel with the most recent results
        Returns:

        """
        pass
