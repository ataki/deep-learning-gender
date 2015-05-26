"""
Runs scheduled tasks as defined in a tasks.py file in the
same directory
"""

import schedule
import time
from tasks import EXPORTED_TASKS

import logging

for job, x, units in EXPORTED_TASKS:
	name = str(job)

	if units == 'sec':
		schedule.every(x).seconds.do(job)
	elif units == 'min':
		schedule.every(x).minutes.do(job)
	elif units == 'hr':
		schedule.every(x).hour.do(job)
	else:
		logging.warning("Skipped task {0}, unknown time units {1}".format(name, units))

	# Log on the side
	if units in ['sec', 'min', 'hr']:
		logging.info("Scheduling {0} for every {1} {2}".format(name, str(x), units))
