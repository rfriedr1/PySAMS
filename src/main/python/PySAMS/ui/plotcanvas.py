from config.logging_conf import logger
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import PyQt5.QtWidgets as QtWidgets
import pandas

# set logger name to the name of the module
logger.name = __name__


class MyPlotCanvas(FigureCanvas):
    """
    Creates a widget of a plot canvas that can be placed in a layout an display plots.

    """

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        logger.debug('MyPlotCanvas: initializing...')

        # create a figure
        fig = Figure(figsize=(width, height), dpi=dpi)
        # add axis to the figure just to show something
        self.ax = fig.add_subplot(111)
        # bind figure to the FigureCanvas by initializing the FigureCanvas Object
        FigureCanvas.__init__(self, fig)
        # set the parent of the canvas
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        logger.debug('MyPlotCanvas: initializing... done')

    def create_plot(self, dataframe: pandas.DataFrame):
        """
        use the data in datamodel to create a plot inside the plotcanvas

        Args:
            dataframe

        Returns:
            None
        """
        logger.debug('MyPlotCanvas: create_plot method started')
        self.ax.cla()
        # convert first and second column of the datamodel to a dataframe
        # get the names of the first two columns
        header = dataframe.columns.values.tolist()
        self.xlabel = header[0]
        self.ylabel = header[1]
        # create scatter plot of the first two columns
        self.ax.scatter(x=dataframe.iloc[:, 0], y=dataframe.iloc[:, 1])
        # add axis labels
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)

        # sns.set()
        # sns.set_style("dark")
        # sns.set_palette('Set2')
        # sns.despine()

        self.draw()

        logger.debug('MyPlotCanvas: create_plot method ended')




