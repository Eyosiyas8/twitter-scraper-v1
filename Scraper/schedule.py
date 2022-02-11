from apscheduler.schedulers.blocking import BlockingScheduler
import os
from index import *
def some_job():
    os.system('/usr/bin/python3 /home/ubuntu/Desktop/OSINT/Twitter/twitterScraper/Scraper/schedule.py')
scheduler = BlockingScheduler()
scheduler.add_job(some_job, 'interval', minutes=1)
scheduler.start()