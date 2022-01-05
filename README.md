# About Twitter_scraper
################################################################
Twitter_scraper is a tool which utilizes the twint scrapping module to scrape tweets as well as replies of tweets. You can scrape the tweets as well as the replies by first provide the username you want to scrape from on the text file named Document located under Authentication folder, then you can start scraping by running the scraper file named index.py
The scraper uses both mongodb and elasticsearch as a backend (i.e. it uses mongodb as a stable db and elasticsearch for its visualization capabilities).
################################################################
# Installation Files (all-in-one)
##########################################################
pip3 install elasticsearch tqdm pymongo parawrap selenium lxml pandas twint
##########################################################
# About Chromedriver
##########################################################
Make sure the chrome webdriver is the same version with your chrome browser
- open google chrome and paste chrome://settings/help 
- search for a chrome webdriver with that specific version number
##########################################################
# For Problematic twint
##########################################################
pip3 install --upgrade -e git+https://github.com/twintproject/twint.git@origin/master#egg=twint
##########################################################
# For more information on twint
##########################################################
https://github.com/twintproject/twint
##########################################################