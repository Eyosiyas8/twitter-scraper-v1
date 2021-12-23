import time
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

#browser = webdriver.chrome('./chromedriver')


def youtube_login(email, password):
    # Browser
    driver = webdriver.Chrome(executable_path=r"C:\Users\User\PycharmProjects\twitterScraper\venv\Scripts\chromedriver\chromedriver.exe")
    driver.get('https://accounts.google.com/ServiceLogin?hl=en&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Fhl%3Den%26feature%3Dsign_in_button%26app%3Ddesktop%26action_handle_signin%3Dtrue%26next%3D%252F&uilel=3&passive=true&service=youtube#identifier')

    # log in
    try:
        driver.find_element(By.CSS_SELECTOR, 'input[type=email]').send_keys(email)
        driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/span").click()
    except:
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='email']")))
        element.send_keys(email)

        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.ID, "submit-button']")))
        element.click()

    time.sleep(2)
    wait = WebDriverWait(driver, 30)
    element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input")))
    element.send_keys(password)

    # waite = WebDriverWait(driver, 30)
    # elements = waite.until(EC.presence_of_element_located((By.XPATH, "//input[@name='password']")))
    # elements.send_keys(password)
    # wait = WebDriverWait(driver, 30)
    #driver.find_element(By.CSS_SELECTOR,"button").click()
    element = wait.until(EC.presence_of_element_located((By.ID, "passwordNext")))
    element.click()

    return driver


def Report_page(driver, urls):
    # Check if there still urls
    if len(urls) == 0:
        print('Youtube Report Bot: Finished!')
        return []

    # Pop a URL from the array
    url = urls.pop()

    # Visite the page
    driver.get(url)
    driver.implicitly_wait(1)

    # Is video avaliable (deleted,private) ?
    # if not check_exists_by_xpath(driver, '//*[@id="movie_player"]'):
    #     return Report_page(driver, urls,)

    # Scroll, wait for load comment box
    #driver.execute_script("window.scrollTo(0, 500);")


    # Lets wait for report page

    time.sleep(1)
    try:
        #driver.execute_script("window.scrollTo(0,0);")
        driver.implicitly_wait(10)
        WebDriverWait(driver, 35).until(EC.presence_of_element_located((By.XPATH,"/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[8]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/yt-icon-button/button"))).click()
    except:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[8]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/yt-icon-button/button"))).click()
    time.sleep(2)
    # Activate box for report
    driver.implicitly_wait(5)
    driver.find_element(By.XPATH,"//tp-yt-paper-item[@role='option']").click()

    # Send report part
    time.sleep(2)
    wait = WebDriverWait(driver, 30)
    report_menu = wait.until(EC.presence_of_element_located((By.NAME,"2")))
    report_menu.click()

    time.sleep(2)
    wait = WebDriverWait(driver, 30)
    try:
        report_menu_send = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/ytd-app/ytd-popup-container/tp-yt-paper-dialog/yt-report-form-modal-renderer/tp-yt-paper-dialog-scrollable/div/div/yt-options-renderer/div/tp-yt-paper-radio-group/tp-yt-paper-dropdown-menu[3]/tp-yt-paper-menu-button/div/div/tp-yt-paper-input/tp-yt-paper-input-container/div[2]/span[2]/tp-yt-iron-icon")))
        report_menu_send.click()
    except:
        wait = WebDriverWait(driver, 30)
    time.sleep(2)
    wait = WebDriverWait(driver, 30)
    try:
        report_menu_send = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/ytd-app/ytd-popup-container/tp-yt-paper-dialog/yt-report-form-modal-renderer/tp-yt-paper-dialog-scrollable/div/div/yt-options-renderer/div/tp-yt-paper-radio-group/tp-yt-paper-dropdown-menu[3]/tp-yt-paper-menu-button/tp-yt-iron-dropdown/div/div/tp-yt-paper-listbox/tp-yt-paper-item[2]")))
        report_menu_send.click()
        report_menu_send.send_keys(Keys.ENTER)
    except:
        WebDriverWait(driver, 30)

    time.sleep(2)
    # Is post ready to be clicked?
    try:
        driver.implicitly_wait(5)
        post = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH,"//div [@id ='submit-button']")))
        post.click()
        posting = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//div['@id=submit-button']")))
        posting.click()
    except:
        wait = WebDriverWait(driver, 40)
        post = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '/html/body/ytd-app/ytd-popup-container/tp-yt-paper-dialog[2]/yt-report-details-form-renderer/div[3]/div[2]')))
        # post.click()
        # posting = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH,'/html/body/ytd-app/ytd-popup-container/tp-yt-paper-dialog[2]/yt-report-details-form-renderer/div[3]/div[2]')))
        # posting.click()



    # Lets wait a bit
    r = np.random.randint(2, 5)
    time.sleep(r)

    # Recursive
    return Report_page(driver, urls)


def random_comment():
    messages = [
        'Whats up?',
        'Nice video!',
        'Yoyoyo'
    ]

    r = np.random.randint(0, len(messages))

    return messages[r]


# def check_exists_by_xpath(driver, xpath):
#     try:
#         driver.find_element_by_xpath(xpath)
#     except NoSuchElementException:
#         return False
#
#     return True


if __name__ == '__main__':
    # Credentials
    email = 'andrewsein123@gmail.com'
    password = 'K@lep@55'

    # List of Urls
    urls = [
        'https://www.youtube.com/watch?v=xiCg7Gsd6Kk',
    ]

    # You can add in a file and import from there
    '''
    inp = open ("urls.txt","r")
    for line in inp.readlines():
            urls.append(line.split())
      '''
    # Login in youtube

    driver = youtube_login(email, password)

    # Random comment
    Report_page(driver, urls)