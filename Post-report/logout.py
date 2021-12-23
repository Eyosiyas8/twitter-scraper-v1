from login import *
# logging out from an account

wait = WebDriverWait(driver, 5)
element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[2]/header/div/div/div/div[2]/div/div/div/div/div[2]")))
element.click()
time.sleep(1)

wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@data-testid='AccountSwitcher_Logout_Button']")))
element.click()
time.sleep(1)

wait = WebDriverWait(driver, 5)
element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div[2]/div[2]/div/span/span")))
element.click()
time.sleep(3)
driver.close