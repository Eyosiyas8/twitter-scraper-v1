from apscheduler.schedulers.blocking import BlockingScheduler
import os
from index import *

# Set an interval for authomatic scraping
def some_job():
    '''
    This function defines the file to run in the interval specified below.
    '''
    os.system(os.path.join(basedir, '/schedule.py'))
scheduler = BlockingScheduler()
scheduler.add_job(some_job, 'interval', minutes=1)
scheduler.start()