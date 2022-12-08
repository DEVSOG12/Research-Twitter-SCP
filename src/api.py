# Importing the libraries
import configparser
import csv
import os
import time
from datetime import datetime
import tweepy

from src.extract_csv import extract_csv

# Read the config file
config = configparser.ConfigParser()
config.read('.././config/config.ini')

# Read the values
api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']
access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

# Authenticate
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Extract the data from the CSV file and store it in a list
data_dict = extract_csv('../data/Oreofe-ScrapeDictionary.csv')
data = extract_csv('../data/Oreofe-Twitter2Scrape.csv')


# Add data to CSV file: containing the Name, Twitter Handle, and the Date of the first Tweet and number of Tweets
def add_data_to_csv(name, twitter_handle, date, num_tweets):
    with open('../outputs/scraped-info.csv', 'a') as k_file:
        writer = csv.writer(k_file)
        writer.writerow([name, twitter_handle, date, num_tweets])


# Create a CSV file to store the scraped data
def create_csv_file():
    with open('../outputs/scraped-info.csv', 'w') as k_file:
        writer = csv.writer(k_file)
        writer.writerow(['Name', 'Twitter Handle', 'Date of First Filtered Tweet', 'Number of Filtered Tweets'])


def run():
    total_duration = 0
    current_duration = 0
    error_count = 0

    for i in data.keys():
        # Check if CSV file exists
        if not os.path.exists('../outputs/scraped-info.csv'):
            create_csv_file()
        print('error_count: ', error_count)
        # Check number of .txt files in ../output folder
        # If the number of files is equal to the number of keys in the data dictionary, then break
        # Else, continue
        print(len(os.listdir('../outputs')))

        # Check if file has already been scraped by check ../output/{username}.txt exists
        # If it does, skip it
        try:
            username = str(data[i][0]).replace('https://twitter.com/', '')  # Get the username from the URL
            print(username)
            with open(f'../outputs/{username}.txt', 'r'):  # Check if file exists
                print('Already scraped')
                continue
        except FileNotFoundError:  # If file does not exist, continue
            pass

        # Check if request have been made within the last 15 minutes
        if current_duration >= (5 * 60):
            current_duration = 0
            #     print('Sleeping for 15 minutes')
            time.sleep(200)
            print('Awake')

        username = data[i][0]  # Get the username from the URL
        if str(username).__contains__('https://twitter.com/'):  # Check if the username is a URL
            username = username.replace('https://twitter.com/', '')  # Get the username from the URL
        else:
            print('Invalid username', data[i][0])
            error_count += 1
            continue

        start_time = datetime.now()
        print("Start time: ", start_time)
        tweets = []
        fetchedTweets = api.user_timeline(screen_name=username, count=200, include_rts=False, tweet_mode='extended',
                                          exclude_replies=True)
        tweets.extend(fetchedTweets)
        lastTweetInList = tweets[-1].id - 1

        while len(fetchedTweets) > 0:
            fetchedTweets = api.user_timeline(screen_name=username, count=200, max_id=lastTweetInList,
                                              include_rts=False, tweet_mode='extended', exclude_replies=True)
            tweets.extend(fetchedTweets)
            lastTweetInList = tweets[-1].id - 1
            print(f"Cached {len(tweets)} tweets so far.")
        #     Stop timer
        end_time = datetime.now()
        print("End time: ", end_time)
        duration = end_time - start_time
        print("Duration: ", duration)
        # Add the duration to the total duration
        current_duration += duration.seconds
        total_duration += duration.seconds

        # Elon Musk's date of control of Twitter
        elon_musk_date = datetime.strptime("2022-10-26 00:00:00+00:00", "%Y-%m-%d %H:%M:%S%z")
        for tweet in tweets:
            tweet_time = datetime.strptime(str(tweet.created_at), '%Y-%m-%d %H:%M:%S%z')
            if tweet_time < elon_musk_date:
                tweets.remove(tweet)

        # Filter tweets if they contain any of the keywords in data_dict
        keywords = list(data_dict.keys())
        keywords = [x[:len(x) - 1] for x in keywords]
        tweets_text = [("Tweet Created on " + str(i.created_at) + " :" + i.full_text + "\n") for i in tweets]
        # print(keywords)
        filtered_tweets = []
        # Check if the tweet contains any of the keywords in list keywords and add it to filtered_tweets using fnmatch
        dateC = None
        tweets_text = tweets_text[::-1]
        for tweet in tweets_text:  # Loop through the tweets
            for keyword in keywords:  # Loop through the keywords
                for word in tweet.split():  # Loop through the words in the tweet
                    if word.startswith(keyword):  # Check if the word starts with the keyword
                        if dateC is None:  # Check if dateC is None
                            dateC = tweet[17:27]  # Get the date of the tweet
                        filtered_tweets.append(tweet)  # Add the tweet to filtered_tweets
                        break
        # TC: O(n^3) :(
        # Write the tweets to a file
        with open(f'../outputs/{username}.txt', 'w') as file:
            for tweet in filtered_tweets:
                file.write(f"{tweet}\n")
        # Add the data to the CSV file
        add_data_to_csv(i, username, dateC, len(filtered_tweets))
