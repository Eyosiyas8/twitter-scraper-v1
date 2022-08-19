from apscheduler.schedulers.blocking import BlockingScheduler
import os
from index import *
def some_job():
    os.system(os.path.join(basedir, '/schedule.py'))
scheduler = BlockingScheduler()
scheduler.add_job(some_job, 'interval', minutes=1)
scheduler.start()