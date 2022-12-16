from apscheduler.schedulers.blocking import BlockingScheduler
import os
from index import *
# from log import *

# Set an interval for authomatic scraping
def scrape_scheduler():
    '''
    This function defines the file to run in the interval specified below.
    '''
    os.system(os.path.join(basedir, 'index.py'))
    # os.system(os.path.join(basedir, 'index_keyword.py'))
scheduler = BlockingScheduler()
try:
    scheduler.add_job(scrape_scheduler, 'interval', minutes=1)
except Exception as e:
    error_log(message)
scheduler.start()
