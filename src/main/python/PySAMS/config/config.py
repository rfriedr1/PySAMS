"""
package that deals with:
- sharing values across modules
- reading and writing of config files for the pySAMS
"""

from config.logging_conf import logger
import os.path
import configparser

# set logger name to the name of the module
logger.name = __name__


class MyConfig(configparser.ConfigParser):
    """
    main class that deals with the configuration
    by loading the necessary files etc etc

    inherits from the configparser Class

    path to ini file is prescribed in class
    """

    def __init__(self):
        logger.debug('perform: __init__')
        logger.debug('instantiate MyConfig class')
        # set path to ini file here
        logger.debug('set path to config file')
        self.config_file_path = os.path.abspath('..\\config.ini')
        self.config_file_path = 'config.ini'
        logger.debug('file path = ' + self.config_file_path)
        # initialize configparser super class
        self.conf = super().__init__()

        # check if everything is fine with the config file
        # also reads the config file
        if self.checkconfig() == False:
            self.writedefaultconfig()   # write default values
            if self.checkconfig():      # check again
               pass
        else:
            # everything is fine
            pass

    def checkconfig(self):
        """
        Check whether config file exists
        and is holding all the necessay information.
        If so sections of the config file are read.

        Returns:
            True = file is present and good to go
            False = something is not ok

        """
        logger.debug('checking config file')
        if os.path.isfile(self.config_file_path):
            logger.debug('config file exists')
            # read ini settings if the settings file exists
            logger.debug('config file path')
            inipath = os.path.abspath(self.config_file_path)  # get the full path just to see that it works
            logger.debug(inipath)

            try:
                # read config file
                logger.debug('reading config file')
                self.read(self.config_file_path)
            except Exception:
                logger.error('error reading config file')
                logger.error('exception: ')
                return False
            else:
                # no exception raised so read the file
                # return sections in ini file
                logger.debug('return section names found in config file')
                for section in self.sections():
                    logger.debug('section: ' + section)
                return True
        else:
            # ini file doesn't exist, create one and fill with some default settings
            logger.error('config file does not exist')
            return False

    def writedefaultconfig(self):
        """
        create a new config file and write the default values

        Returns:
            None

        """
        logger.debug('create default config file')
        if os.path.isfile(self.config_file_path):
            logger.debug('config file already exists')
        else:
            logger.debug("config file doesn't exists")
            f = open(self.config_file_path, 'w')
            f.write('[database]\r')
            f.write('dbhost = 192.168.123.30\r')
            f.write('dbuser = mams\r')
            f.write('dbpasswd = Micadas.1\r')
            f.write('dbname = db_dmams\r')
            f.write('[paths]\r')
            f.write('path_to_reports_on_server =\r')
            f.write('path_to_reports_templates =\r')
            f.write('path_to_reports_local =\r')
            f.write('path_to_images_in_server =\r')
            f.write('path_to_docs_on_server =\r')
            f.close()
            logger.debug('default values in config written')


# already instantiate the MyConfig Object here
# that allows sharing this single instance across modules
logger.debug('Instantiate the myconfig object instance in the config module')
myconfig = MyConfig()

