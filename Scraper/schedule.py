from apscheduler.schedulers.blocking import BlockingScheduler
import os
import configparser
# from index_keyword import *
# from log import *
basedir = os.path.dirname(os.path.abspath(__file__))
config = configparser.ConfigParser()
elements_file = os.path.join(basedir, '../Authentication/elements_iteration.ini')
config.read(elements_file)
scrape_interval = config['scrape_interval']
# Set an interval for authomatic scraping
def scrape_scheduler():
    '''
    This function defines the file to run in the interval specified below.
    '''
    # os.system(os.path.join(basedir, 'index.py'))
    file_path = os.path.join(basedir, 'index_keyword.py')
    file_path1 = os.path.join(basedir, 'index.py')
    os.system('python3 ' + file_path)
    os.system('python3 ' + file_path1)
scheduler = BlockingScheduler()
try:
    scheduler.add_job(scrape_scheduler, 'interval', minutes = int(scrape_interval.get('scraper')))
except Exception as e:
    error_log(message)
scheduler.start()
