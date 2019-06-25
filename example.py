import csvhound
# import logging

csvhound.set_stream_logger('csvhound')

# how to override library logging level:
# logging.getLogger('csvhound').setLevel(logging.WARNING)

csvhound.do_something()
