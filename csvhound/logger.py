import logging

# set up logging
# TODO move to helper function/module?

# create new logger with library's name
logger = logging.getLogger(__package__)

# set null handler
logger.addHandler(logging.NullHandler())

# set logging level
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%m/%d/%Y %I:%M:%S %p')

# create a fileHandler
fileHandler = logging.FileHandler(filename='/Users/christie/Work/csv-hound/csvhound.log')
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)
# create a new console stream handler, set its debug level, formatting and attach
# consoleHandler = logging.StreamHandler()
# consoleHandler.setLevel(logging.DEBUG)
# logger.addHandler(consoleHandler)
# consoleHandler.setFormatter(formatter)

logger.debug('handlers added')
