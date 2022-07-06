# configuration file that configures logging for the whole project
# import this file into any module in order to have logging available

import logging

#logging.basicConfig(filename=logfile, level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger('mainlog')
# general logger level
logger.setLevel(logging.DEBUG)

# setup file logging #######################################
logfile = 'logfile.log'
# empty file first
open(logfile, 'w').close()
logfilehandler = logging.FileHandler(logfile)
# set log format for file logging
logformat = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(funcName)s:%(lineno)d | %(message)s')
logfilehandler.setFormatter(logformat)
# set level for file logging
logfilehandler.setLevel(logging.DEBUG)
# tell logger to use this logfile
logger.addHandler(logfilehandler)

# setup console logging