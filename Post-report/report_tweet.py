from login import *
import csv
from datetime import datetime
from pymongo import MongoClient
import pandas as pd

suspiciousIdList = []
usernameList = []
client = MongoClient('mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false')
db = client['twitter-data']
collection = db['twitter']
login()
try:
    wait = WebDriverWait(driver, 20)
    element = wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div/div/div/div[2]/header/div/div/div/div[1]/div[2]/nav/a[2]")))
    element.click()
except:
    NoSuchElementException

tweet_ids = "twitter-reporting-ids.csv"


def report_tweet():
    with open(tweet_ids, 'r+', encoding="utf-8") as f:
        reader = csv.DictReader(x.replace('\0', '') for x in f)

        for row in reader:
            print(row)
            id = row['id']
            reported_by = row['user_id']
            url = "https://twitter.com/%s/%s/%s" % ('username', 'status', id)
            driver.get(url)
            time.sleep(2)
            driver.refresh()
            time.sleep(2)

            try:
                time.sleep(2)
                wait = WebDriverWait(driver, 10)
                element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='caret']")))
                element.click()
                time.sleep(1)
            except:
                wait = WebDriverWait(driver, 10)
                element = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                     "//div[@class='css-18t94o4 css-1dbjc4n r-1niwhzg "
                                                                     "r-sdzlij r-1phboty r-rs99b7 r-15ysp7h r-4wgw6l "
                                                                     "r-1ny4l3l r-ymttw5 r-o7ynqc r-6416eg "
                                                                     "r-lrvibr']")))
                element.click()
                time.sleep(1)

                wait = WebDriverWait(driver, 10)
                element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='caret']")))
                element.click()
                time.sleep(1)

            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='report']")))
            element.click()
            time.sleep(1)

            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
            driver.switch_to.frame(element)
            time.sleep(1)

            try:
                wait = WebDriverWait(driver, 5)
                element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/form/button[5]")))
                element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/form/button[4]")))
                element.click()
            except:
                wait = WebDriverWait(driver, 10)
                element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/form/button[3]")))
                element.click()

            wait = WebDriverWait(driver, 20)
            element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/form/button[4]")))
            element.click()
            time.sleep(1)

            wait = WebDriverWait(driver, 20)
            element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/form/button[3]")))
            element.click()
            time.sleep(1)

            wait = WebDriverWait(driver, 20)
            element = wait.until(EC.presence_of_element_located((By.XPATH, ".//input[@class='tweetSelector']")))
            element.click()
            time.sleep(1)
            try:
                try:
                    wait = WebDriverWait(driver, 10)
                    element = wait.until(
                        EC.presence_of_element_located((By.XPATH, ".//button[contains(text(), 'Add')]")))
                    element.click()
                except:
                    wait = WebDriverWait(driver, 10)
                    element = wait.until(EC.presence_of_element_located((By.XPATH, ".//button[@id='attach_tweets']")))
                    element.click()
            except:
                try:
                    wait = WebDriverWait(driver, 10)
                    element = wait.until(
                        EC.presence_of_element_located((By.XPATH, ".//button[contains(text(), 'Skip')]")))
                    element.click()
                except:
                    wait = WebDriverWait(driver, 10)
                    element = wait.until(EC.presence_of_element_located((By.XPATH, ".//button[@class='skip-btn']")))
                    element.click()

            driver.switch_to.parent_frame()
            time.sleep(2)
            wait = WebDriverWait(driver, 20)
            element = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                 "/html/body/div[1]/div/div/div[1]/div["
                                                                 "2]/div/div/div/div/div/div[2]/div["
                                                                 "2]/div/div/div/div[1]/div/div/div/div/div/div["
                                                                 "3]/div")))
            element.click()
            time.sleep(1)

            id = id.replace('\n', '')

            collection.update_many({}, {'$set': {
                'tweets.$[elem].reporting': {'is_reported': True, 'reporting_date': datetime.today(),
                                             'reported_by': reported_by}}}, array_filters=[{"elem.id": {'$eq': id}}])

            collection.update_many({}, {'$set': {
                'tweets.$[].replies.$[elem].reporting': {'is_reported': True, 'reporting_date': datetime.today(),
                                                         'reported_by': reported_by}}},
                                   array_filters=[{"elem.id": {'$eq': id}}])

            df = pd.read_csv(tweet_ids)
            df = df.iloc[1:]
            df.pop('Unnamed: 0')
            df.to_csv(tweet_ids)


report_tweet()
driver.close()
