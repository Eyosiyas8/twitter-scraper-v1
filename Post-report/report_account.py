from login import *
login()

f=open("/home/osint/Desktop/OSINT/Twitter/twitterScraper/Authentication/reporting.txt","r")
lines=f.readlines()
for username in lines:
    time.sleep(5)
    driver.get('https://www.twitter.com/'+username)
    print(username)

    wait = WebDriverWait(driver, 20)
    element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/div[1]/div/div[1]/div/div[1]")))
    element.click()

    time.sleep(2)
    wait = WebDriverWait(driver, 20)
    element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[5][@role='menuitem']")))
    element.click()

    wait = WebDriverWait(driver, 20)
    element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
    driver.switch_to.frame(element)
    time.sleep(1)

    wait = WebDriverWait(driver, 20)
    element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/form/button[6]")))
    element.click()

    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/form/button[4]")))
    element.click()

    wait = WebDriverWait(driver, 20)
    element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/form/button[3]")))
    element.click()

    wait = WebDriverWait(driver, 20)
    element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/form/div/div[2]/button[1]")))
    element.click()

    time.sleep(1)

    driver.switch_to.parent_frame()
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/div/div/div/div[3]/div/div/span/span")))
    element.click()
time.sleep(3)
driver.close