import time

from login import *
login()
f=open("/home/osint/Desktop/OSINT/Twitter/twitterScraper/Authentication/Document.txt","r")
line=f.readlines()
username=line[0]
time.sleep(5)

driver.get('https://www.twitter.com/'+username)
print(username)
time.sleep(1)
driver.refresh()
time.sleep(1)
wait = WebDriverWait(driver, 20)
element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[2]/section/div/div/div[1]/div/div/article/div/div/div/div[2]/div[2]/div[2]/div[3]/div/div[3]/div")))
element.click()

time.sleep(3)
driver.close()