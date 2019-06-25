import logging
import csvhound.core

def set_stream_logger(name='csvhound', level=logging.DEBUG, format_string=None):
    """
    Add a stream handler for library.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if format_string is None:
        format_string = "%(asctime)s - %(levelname)s - %(message)s"

    # create a new console stream handler, set its debug level, formatting and attach
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(level)
    formatter = logging.Formatter(format_string, '%m/%d/%Y %I:%M:%S %p')
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)

# create new logger with library's name
logger = logging.getLogger(__name__)

# set null handler
logger.addHandler(logging.NullHandler())

logger.debug(__name__ + ' module loaded')

def do_something():
    logger.debug('do something')
