import time

from login import *

login()

# Read a content from a file and post it
def post():
    f=open("/home/osint/Desktop/OSINT/Twitter/twitterScraper/Authentication/tweets.txt","r")
    line=f.readlines()
    first_tweet=line[0]

    wait = WebDriverWait(driver, 5)
    element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div/div/div/div/div/span/br')))
    element.send_keys(first_tweet)
    time.sleep(1)

    wait = WebDriverWait(driver, 5)
    element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]/div/span/span")))
    element.click()
    time.sleep(1)


post()
# logging out from an account

wait = WebDriverWait(driver, 5)
element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/header/div/div/div/div[2]/div/div/div/div/div[2]")))
element.click()

wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@data-testid='AccountSwitcher_Logout_Button']")))
element.click()

wait = WebDriverWait(driver, 5)
element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div[2]/div[2]/div/span/span")))
element.click()

time.sleep(3)
driver.close()