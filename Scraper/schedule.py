from apscheduler.schedulers.blocking import BlockingScheduler
import os
from index import *
from log import *

# Set an interval for authomatic scraping
def some_job():
    '''
    This function defines the file to run in the interval specified below.
    '''
    os.system(os.path.join(basedir, '/index.py'))
scheduler = BlockingScheduler()
try:
    scheduler.add_job(some_job, 'interval', minutes=1)
except Exception as e:
    system_log(message)
scheduler.start()