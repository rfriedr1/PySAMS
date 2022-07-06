from config.logging_conf import logger
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
import plots.qc.qcplots as qcplots
import plots.stat.statplots as statplots

# set logger name to the name of the module
logger.name = __name__


class PlotWindow(QtWidgets.QMainWindow):
    """
    main class for the plot window (formerly the AMSDataInspector).

    It is intended to generate plots of various QC or
    statistical data directly retrieved from a database.

    Args:
        None

    Returns:
        None
    """

    # TODO add function to create all plots at once

    def __init__(self):
        """
        Initialize the App object.

        Create a instance attribute that holds the db parameters.
        In that way the db_params are only valid for this instance of the App

        Create all the windows elements (buttons etc etc)
        """
        logger.info('create PlotWindow')
        super().__init__()  # method calls are directed to the parent

        # prepare basic windows settings
        self.title = 'Plot Window'
        self.left = 10
        self.top = 10
        self.width = 300
        self.height = 480

        # create window
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # initialize event handler for button clicks and so on
        # eventhandler = EventHandler()

        # create statusbar
        self.statusbar = QtWidgets.QStatusBar()  # create a ststusbar
        self.setStatusBar(self.statusbar)  # assign statusbar to the MainWindow
        self.statusbar.showMessage('AMS Data Inspector', 2000)

        # create the central widget that goes into the mainwindow
        centralWidget = QtWidgets.QWidget()

        # central widget: add a label
        label = QtWidgets.QLabel('Choose Plot', self)

        # central widget: add a list widget
        self.listBoxItems = ['-- do all plots --',
                             '-- all QC plots --',
                             'received samples',
                             'projects per year',
                             'measured samples',
                             'overall age precision',
                             'oxas blanks stdev per magazine',
                             'age precision over time',
                             'age histogram',
                             'materials',
                             'turnaround times histogram (select year)',
                             'express samples',
                             'bone collagen distribution',
                             'MAG parameters',
                             'AGE parameters',
                             'blank values',
                             'IAEA C1',
                             'IAEA C2',
                             'IAEA C3',
                             'IAEA C6',
                             'ICOS HEI3',
                             'ICOS HEI10',
                             'horses']
        self.listBox = QtWidgets.QListWidget(self)
        self.listBox.addItems(self.listBoxItems)
        self.listBox.itemSelectionChanged.connect(self.list_selection_on_change)

        # central widget: create a button
        button = QtWidgets.QPushButton('Plot', self)
        button.setToolTip('create the selected plot')
        button.move(100, 200)
        button.clicked.connect(lambda: self.btn_on_click(self.listBox))

        # central widget: combine all into a layout
        self.vlayout = QtWidgets.QVBoxLayout()
        self.vlayout.setContentsMargins(0, 10, 0, 0)
        self.vlayout.addWidget(label)
        self.vlayout.addWidget(self.listBox)
        self.vlayout.addWidget(button)

        # central widget: assign layout to central widget
        centralWidget.setLayout(self.vlayout)
        self.setCentralWidget(centralWidget)

        # actually show the UI
        self.show()

    # pyqt slots for handling the events
    @QtCore.pyqtSlot()
    def list_selection_on_change(self):
        sender = self.sender()
        self.statusBar().showMessage('plotting #' + str(sender.currentRow()))

    @QtCore.pyqtSlot()
    def btn_on_click(self, listBox):
        sender = self.sender()
        logger.debug('plotwindow -- list of plots button click')
        logger.debug(str(listBox.currentRow()))
        # create the plots depending on the selection of the list box
        if listBox.currentRow() == 0:  # this creates all plots at ones
            # show a progress dialog with 18 steps (number of plots to be processed)
            progressdlg = QtWidgets.QProgressDialog('creating plots...', 'stop', 0, 18)
            progressdlg.setWindowModality(QtCore.Qt.WindowModal)
            progressdlg.setMinimumDuration(0)

            # in order to be able to check the 'stop' button run the commands inside of a loop
            proceed = True
            while proceed:
                progressdlg.setValue(0)
                fig = statplots.plot_received()
                progressdlg.setValue(1)
                if progressdlg.wasCanceled():
                    break
                fig = statplots.plot_projects_per_year()
                progressdlg.setValue(2)
                if progressdlg.wasCanceled():
                    break
                fig = statplots.plot_throughput()
                progressdlg.setValue(3)
                if progressdlg.wasCanceled():
                    break
                fig = statplots.plot_age_precision()
                progressdlg.setValue(4)
                if progressdlg.wasCanceled():
                    break
                fig = statplots.plot_oxas_stdev_mag()
                progressdlg.setValue(5)
                if progressdlg.wasCanceled():
                    break
                fig = statplots.plot_age_precision_time()
                progressdlg.setValue(6)
                if progressdlg.wasCanceled():
                    break
                fig = statplots.plot_age_hist()
                progressdlg.setValue(7)
                if progressdlg.wasCanceled():
                    break
                fig = statplots.plot_material()
                progressdlg.setValue(8)
                if progressdlg.wasCanceled():
                    break
                fig = statplots.plot_turnaround()
                progressdlg.setValue(9)
                if progressdlg.wasCanceled():
                    break
                fig = statplots.plot_express_samples()
                progressdlg.setValue(10)
                if progressdlg.wasCanceled():
                    break
                fig = statplots.plot_bone_collagen()
                progressdlg.setValue(11)
                if progressdlg.wasCanceled():
                    break
                fig = statplots.plot_MAG_params()
                progressdlg.setValue(12)
                if progressdlg.wasCanceled():
                    break
                fig = statplots.plot_AGE_params()
                progressdlg.setValue(13)
                if progressdlg.wasCanceled():
                    break
                fig = qcplots.plot_blanks()
                progressdlg.setValue(14)
                if progressdlg.wasCanceled():
                    break
                fig = qcplots.plot_c1()
                progressdlg.setValue(15)
                if progressdlg.wasCanceled():
                    break
                fig = qcplots.plot_c2()
                progressdlg.setValue(16)
                if progressdlg.wasCanceled():
                    break
                fig = qcplots.plot_c3()
                progressdlg.setValue(17)
                if progressdlg.wasCanceled():
                    break
                fig = qcplots.plot_c6()
                progressdlg.setValue(18)
                if progressdlg.wasCanceled():
                    break
                fig = qcplots.plot_hei3()
                progressdlg.setValue(19)
                if progressdlg.wasCanceled():
                    break
                fig = qcplots.plot_hei10()
                progressdlg.setValue(20)
                if progressdlg.wasCanceled():
                    break
                fig = qcplots.plot_horses()
                progressdlg.setValue(21)
                proceed = False  # stop loop and get out of this if
        elif listBox.currentRow() == 1:  # this creates all qc plots at ones
            # show a progress dialog with 6 steps (number of plots to be processed)
            progressdlg = QtWidgets.QProgressDialog('creating plots...', 'stop', 0, 6)
            progressdlg.setWindowModality(QtCore.Qt.WindowModal)
            progressdlg.setMinimumDuration(0)
            # in order to be able to check the 'stop' button run the commands inside of a loop
            proceed = True
            while proceed:
                progressdlg.setValue(0)
                fig = qcplots.plot_blanks()
                progressdlg.setValue(1)
                if progressdlg.wasCanceled():
                    break
                fig = qcplots.plot_c1()
                progressdlg.setValue(2)
                if progressdlg.wasCanceled():
                    break
                fig = qcplots.plot_c2()
                progressdlg.setValue(3)
                if progressdlg.wasCanceled():
                    break
                fig = qcplots.plot_c3()
                progressdlg.setValue(4)
                if progressdlg.wasCanceled():
                    break
                fig = qcplots.plot_c6()
                progressdlg.setValue(5)
                if progressdlg.wasCanceled():
                    break
                fig = qcplots.plot_horses()
                progressdlg.setValue(6)
                proceed = False  # stop loop and get out of this if
        if listBox.currentRow() == 2:
            fig = statplots.plot_received()
        if listBox.currentRow() == 3:
            fig = statplots.plot_projects_per_year()
        elif listBox.currentRow() == 4:
            fig = statplots.plot_throughput()
        elif listBox.currentRow() == 5:
            fig = statplots.plot_age_precision()
        elif listBox.currentRow() == 6:
            fig = statplots.plot_oxas_stdev_mag()
        elif listBox.currentRow() == 7:
            fig = statplots.plot_age_precision_time()
        elif listBox.currentRow() == 8:
            fig = statplots.plot_age_hist()
        elif listBox.currentRow() == 9:
            fig = statplots.plot_material()
        elif listBox.currentRow() == 10:
            fig = statplots.plot_turnaround()
        elif listBox.currentRow() == 11:
            fig = statplots.plot_express_samples()
        elif listBox.currentRow() == 12:
            fig = statplots.plot_bone_collagen()
        elif listBox.currentRow() == 13:
            fig = statplots.plot_MAG_params()
        elif listBox.currentRow() == 14:
            fig = statplots.plot_AGE_params()
        elif listBox.currentRow() == 15:
            fig = qcplots.plot_blanks()
        elif listBox.currentRow() == 16:
            fig = qcplots.plot_c1()
        elif listBox.currentRow() == 17:
            fig = qcplots.plot_c2()
        elif listBox.currentRow() == 18:
            fig = qcplots.plot_c3()
        elif listBox.currentRow() == 19:
            fig = qcplots.plot_c6()
        elif listBox.currentRow() == 20:
            fig = qcplots.plot_hei3()
        elif listBox.currentRow() == 21:
            fig = qcplots.plot_hei10()
        elif listBox.currentRow() == 22:
            fig = qcplots.plot_horses()

        # somehow this is not needed, plots are created anyway

        # create the plot canvas object where the figure will be displayed
        # self.plotcanvas = plotcanvas.MyPlotCanvas(parent=self, width=5, height=4)
        # send figure to canvas
        # self.plotcanvas.create_plot(fig)
