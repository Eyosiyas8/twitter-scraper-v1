from login import *
login()

f=open("/home/osint/Desktop/OSINT/Twitter/twitterScraper/Authentication/tweets.txt")
line=f.readlines()
username=line[0]
time.sleep(5)

try:
    wait = WebDriverWait(driver, 20)
    element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/header/div/div/div/div[1]/div[2]/nav/a[2]")))
    element.click()
    time.sleep(1)
except:
    NoSuchElementException

wait = WebDriverWait(driver, 20)
element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[2]/div/div/div/form/div[1]/div/div/label/div[2]/div/input")))
element.send_keys("#Nomore")
element.send_keys(Keys.ENTER)
time.sleep(2)

wait = WebDriverWait(driver, 20)
element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/section/div/div/div[8]/div/div/article/div/div/div/div[2]/div[1]")))
element.click()
time.sleep(1)

wait = WebDriverWait(driver, 20)
element = wait.until(EC.presence_of_element_located((By.XPATH, "//br")))
element.send_keys("#Nomore ")
time.sleep(1)
#upload_file.sendKeys("C:/Users/User/Pictures.jfif")

'''wait = WebDriverWait(driver, 20)
element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/main/div/div/div/div/div/div[2]/section/div/div/div[1]/div/div[2]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div/div[1]/div[1]")))
element.click()'''

wait = WebDriverWait(driver, 20)
element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='tweetButtonInline']/div/span")))
element.click()
time.sleep(1)


time.sleep(3)
driver.close()