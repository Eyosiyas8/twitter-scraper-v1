import csv
from timeline_scraper_new import *
def scrape_replies(username, tweet_link):
    # file = open('../csv_files/twets_'+username+'.csv')
    tweet_data = []
    print('the data is ',tweet_link)
    # print('askdjf;lkasjdf;lakjsdf;ljasd;lkjfalkdsjflaksdjfaslkjdf;as',record)
    # print('askdjf;lkasjdf;lakjsdf;ljasd;lkjfalkdsjflaksdjfaslkjdf;as',record[1])
    driver.get(tweet_link)
    # Define the URL for the user's timeline
    # Find all the tweet elements on the page
    reply_data = []
    tweet_ids = set()
    # last_position = driver.execute_script('return window.pageYOffset;')
    scrolling = True
    x=0
    y=1800
    while scrolling:
        # wait = WebDriverWait(driver, 1)
        # element = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//article[@data-testid = "tweet"]')))
        # print(len(element))
        
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        tweet_elements = soup.find_all('article', attrs={'data-testid': 'tweet'})
        print(len(tweet_elements))
        time.sleep(5)
        for tweet_element in tweet_elements:
            dom = etree.HTML(str(tweet_element))
            tweet = scrape_user_timeline(username, dom)
            if tweet and tweet[2] != None or tweet[3] != None:
                tweet_id = ''.join(tweet)
                if tweet_id not in tweet_ids:
                    tweet_ids.add(tweet_id)
                    reply_data.append({
                'username': tweet[0],
                'name': tweet[1], 'tweet_id': tweet[2], 'tweet_link': tweet[3], 'conversation_id': tweet[4], 'date':tweet[5], 'tweet': tweet[6], 'image_link': tweet[7], 'hashtags': tweet[8], 'mentions': tweet[9], 'link': tweet[10],
                'replies_count': tweet[11],
                'retweets_count': tweet[12], 'likes_count': tweet[13], 'views_count': tweet[14],
                'replies': [], 'reporting': {'is_reported': False, 'reporting_date': None, 'reported_by': None}})
        scroll_attempt = 0
        try:
            if len(reply_data) >= 0 and len(reply_data) < 5:
                pass
            else:
                break
        except:
            pass
        # while True:
            # check scroll position
        last_position = driver.execute_script('return window.pageYOffset;')
        print(last_position)
        while True:
            time.sleep(1)
            driver.execute_script('window.scrollTo({0}, {1});'.format(x, y))
            x+=1000
            y+=1000
            curr_position = driver.execute_script('return window.pageYOffset;')
            print(curr_position)
            if last_position == curr_position:
                scroll_attempt=+1

                # end of scroll region
                if scroll_attempt >= 3:
                    scrolling = False
                    break
                else:
                    time.sleep(2) # attempt to scroll again
            else:
                last_position = curr_position
                break
            time.sleep(1)
        
    tweet_data.extend(reply_data)
    print('this is all the tweet data',tweet_data)
    return tweet_data

        # with open(csv_reply, 'a', newline='', encoding='utf-8') as f:
        #     header = ['Fullname', 'Username', 'Tweet_ID', 'Tweet_Link', 'Conversation_ID', 'Timestamp', 'Tweets', 'Image', 'Hashtags', 'Mentions', 'Link', 'Number_of_replies', 'Number_of_retweets', 'Number_of_likes', 'Number_of_views']
        #     writer = csv.writer(f)
        #     writer.writerow(header)
        #     writer.writerows(tweet_data)