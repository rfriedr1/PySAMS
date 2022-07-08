"""
This is the UI that displays the SplashScreen
"""

from config.logging_conf import logger
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore


# set logger name to the name of the module
logger.name = __name__


class MySplashScreen(QtWidgets.QSplashScreen):
    """
    create a splash screen

    A splash screen is displayed showing the progress of loading
    the settings and DB connection etc

    Returns:
        None
    """

    def __init__(self, *args):
        logger.debug('MySplashScreen -- create MySplashScreen Window')
        super(MySplashScreen, self).__init__(*args)
        # self.setWindowTitle('Startup PySAMS')
        # read image that is used for the splash screen background
        splash_pix = QtGui.QPixmap('ui/icons/PySamsSplash.png')
        # splash_pix = QtGui.QPixmap(appctxt.get_resource('PySamsSplash.png'))  #when packing with fbs resources are loaded like this
        # the splash screens background
        self.setPixmap(splash_pix)
        # make the splash screen sit on top
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        # mask the corners of the splash screen in case the image is not rectangular
        self.setMask(splash_pix.mask())