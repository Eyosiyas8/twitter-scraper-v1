import csv
from timeline_scraper_new import *
def scrape_replies(username, tweet_link, tweet_texts):
    # file = open('../csv_files/twets_'+username+'.csv')
    tweet_data = []
    print('the data is ',tweet_link)
    print('tweet text is ',tweet_texts)
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
    last_position = driver.execute_script('return window.pageYOffset;')
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
            print('the tweet is ',tweet[6])
            if tweet and tweet[2] != None or tweet[4] != None:
                tweet_id = ''.join(tweet)
                if tweet_id not in tweet_ids:
                    tweet_ids.add(tweet_id)
                    if tweet[6] in tweet_texts:
                        tweet[6] = tweet_texts
                    if tweet[5] == 'None':
                        continue
                    else:
                        reply_data.append({
                'username': tweet[0],
                'name': tweet[1], 'tweet_id': tweet[2], 'tweet_link': tweet[3], 'conversation_id': tweet[4], 'date':tweet[5], 'tweet': tweet[6], 'image_link': tweet[7], 'hashtags': tweet[8], 'mentions': tweet[9], 'link': tweet[10],
                'replies_count': tweet[11],
                'retweets_count': tweet[12], 'likes_count': tweet[13], 'views_count': tweet[14],
                'replies': [], 'reporting': {'is_reported': False, 'reporting_date': None, 'reported_by': None}})
        try:
            if len(reply_data) >= 0 and len(reply_data) < 5:
                pass
            else:
                break
        except:
            pass
        # while True:
            # check scroll position
        reply_scroll_attempt = 0
        print('Last position reply ',last_position)
        while True:
            # try:
            #     driver.execute_script('window.scrollTo({0}, {1});'.format(x, y))
            # except:
            #     scrolling = False
            #     break
            time.sleep(1)
            driver.execute_script('window.scrollTo({0}, {1});'.format(x, y))
            x+=1000
            y+=1000
            curr_position = driver.execute_script('return window.pageYOffset;')
            print('current position reply ', curr_position)
            if last_position == curr_position:
                print('try scroll again')
                reply_scroll_attempt+=1
                print('scroll atempt is ',reply_scroll_attempt)

                # end of scroll region
                if reply_scroll_attempt >= 3:
                    print('scroll attempt reached 3 times')
                    scrolling = False
                    break
                else:
                    time.sleep(2) # attempt to scroll again
            else:
                last_position = curr_position
                print('scrolling again ')
                break
        # if scrolling==False:
        #     print('scrolling is false, so it should terminate.')
        #     break        
    tweet_data.extend(reply_data)
    print('this is all the tweet data',tweet_data)
    return tweet_data

        # with open(csv_reply, 'a', newline='', encoding='utf-8') as f:
        #     header = ['Fullname', 'Username', 'Tweet_ID', 'Tweet_Link', 'Conversation_ID', 'Timestamp', 'Tweets', 'Image', 'Hashtags', 'Mentions', 'Link', 'Number_of_replies', 'Number_of_retweets', 'Number_of_likes', 'Number_of_views']
        #     writer = csv.writer(f)
        #     writer.writerow(header)
        #     writer.writerows(tweet_data)