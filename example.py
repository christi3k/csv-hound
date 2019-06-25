import csvhound
# import logging

csvhound.set_stream_logger('csvhound')

# how to override library logging level:
# logging.getLogger('csvhound').setLevel(logging.WARNING)

csvhound.core.do_another_thing()

model = csvhound.core.BaseHound()
table = model.get_table_from_file('sample-data/pydata-event.csv')
model.describe_table()
model.distinct_values('Size', with_count=False)
# table.print_structure()

csvhound.do_something()
