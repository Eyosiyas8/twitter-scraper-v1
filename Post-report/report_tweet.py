from login import *

from pymongo import MongoClient
suspiciousIdList = []
usernameList = []
client = MongoClient('mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false')
db = client['twitter-data']
collect = db['twitter']
results = collect.find({"tweets.replies.sentiment":""})
#print(results)
for obj in collect.find({"tweets.replies.sentiment":"low negative"}, {'tweets.replies.id':1, 'tweets.replies.sentiment':1, 'tweets.replies.username':1}):
  tweets = (obj['tweets'])
  for tweet in tweets:
    replies = tweet['replies']
    for reply in replies:
      if reply['sentiment'] == 'negative':
        print(reply)
        suspiciousIdList.append(reply['id'])
        usernameList.append(reply['username'])
        print()
login()

try:
    wait = WebDriverWait(driver, 20)
    element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/header/div/div/div/div[1]/div[2]/nav/a[2]")))
    element.click()
except:
    NoSuchElementException

def report_tweet():
  for id in suspiciousIdList:
    url = "https://twitter.com/%s/%s/%s" % ('username', 'status', id)
    driver.get(url)
    time.sleep(2)
    driver.refresh()
    time.sleep(2)

    try:
      time.sleep(2)
      wait = WebDriverWait(driver, 10)
      element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/main/div/div/div/div/div/div[2]/section/div/div/div[2]/div/div[1]/article/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/div/div")))
      element.click()
      time.sleep(1)
    except:
      continue
      '''wait = WebDriverWait(driver, 10)
      element = wait.until(EC.presence_of_element_located((By.XPATH,
                                                           "/html/body/div/div/div/div[2]/main/div/div/div/div/div/div[2]/section/div/div/div[2]/div/div/article/div/div/div/div[2]/div/div[2]/div/div[2]/div/div/span")))
      element.click()
      time.sleep(1)

      wait = WebDriverWait(driver, 10)
      element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/main/div/div/div/div/div/div[2]/section/div/div/div[2]/div/div[1]/article/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div/div/div")))
      element.click()
      time.sleep(1)'''

    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='report']")))
    element.click()
    time.sleep(1)

    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
    driver.switch_to.frame(element)
    time.sleep(1)

    element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/form/button[3]")))
    element.click()
    time.sleep(1)

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
        element = wait.until(EC.presence_of_element_located((By.XPATH, ".//button[contains(text(), 'Add')]")))
        element.click()
      except:
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.XPATH, ".//button[@id='attach_tweets']")))
        element.click()
    except:
      try:
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.XPATH, ".//button[contains(text(), 'Skip')]")))
        element.click()
      except:
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.XPATH, ".//button[@class='skip-btn']")))
        element.click()

    driver.switch_to.parent_frame()
    time.sleep(2)
    wait = WebDriverWait(driver, 20)
    element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div/div[3]/div")))
    element.click()
    time.sleep(5)

report_tweet()
driver.close()