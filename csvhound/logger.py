import logging

# set up logging
# TODO move to helper function/module?

# create new logger with library's name
logger = logging.getLogger(__name__)

# set null handler
logger.addHandler(logging.NullHandler())

# set logging level
logger.setLevel(logging.DEBUG)

# create a new console stream handler, set its debug level, formatting and attach
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)
logger.addHandler(consoleHandler)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%m/%d/%Y %I:%M:%S %p')
consoleHandler.setFormatter(formatter)
