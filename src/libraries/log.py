"""
Circular logger to get the trace where is necessary get extra information about the process
"""
from libraries import *

INFO_LOG_FILENAME = 'info_log.log'

infoLogger = lg.getLogger('infolog')
infoLogger.setLevel(lg.DEBUG)

# Add the log message handler to the logger
infoHandler = lh.RotatingFileHandler(INFO_LOG_FILENAME, maxBytes=500000, backupCount=5)
infoLogger.addHandler(infoHandler)




