''' This is the python code to fetch tweets using twint
by providing the date durations and the search keywords based on which the 
tweets must be fetched
The tweets fetched are preprocessed using NLP operations such as remove stopwords, numbers, urls, short words, punctuations, twitter handles, etc
The tweets will be saved in excel files which must be combined using another python file
'''

###Necessary modules that must be installed before executing this code
'''
pip install textblob
python -m textblob.download_corpora
pip install nest_asyncio
pip install --upgrade --user -e git+https://github.com/twintproject/twint.git@origin/master#egg=twint
pip install aiohttp
pip install aiodns
pip install elasticsearch
pip install pysocks
pip install pandas>=0.23.0
pip install aiohttp_socks
pip install schedule
pip install geopy
pip install optimuspyspark
pip install beautifulsoup4
pip install cchardet
pip install spacy
python -m spacy download en_core_web_sm
pip install textacy
pip install pyenchant
'''
####Importing the necessary modules
import re
from textblob import TextBlob
import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import SnowballStemmer, PorterStemmer, WordNetLemmatizer
from nltk import pos_tag
### NLP files which must downloaded when executing the first time in a system, consists of stopwords files, punctuation files
#nltk.download('stopwords')
#nltk.download('wordnet')
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
import string
import seaborn as sns
import itertools
import collections
from datetime import datetime, timedelta, date
import twint###Module to fetch twitter tweets
import nest_asyncio###Module to add some delay while fetching tweets
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import json
import xlsxwriter###To write data into excelsheets
import spacy###Similar to ntlk modules consists of various operations for NLP and also has a sentiment analyzer
import textacy
from time import sleep
import enchant##Module which has a dictionary and if an word is english or not can be determined


''' Method to set up the twint and search for the result, configure the twint with the date duration and search keywords and other parameters
The input parameters are the start date(Since), end date(until) and the query for searching tweets  '''
def twint_configuration_and_search(start_date,end_date,columns):
    print(start_date)
    print(end_date)
    ####Twint scrapping tool coding which is an advanced scarpping tool
    nest_asyncio.apply()# to solve compatibility issues with notebooks and runtime errors
    c = twint.Config()#setting up twint config
    #First set of keywords for Telstra
    #c.Search = '(TLS AND ASX) OR (asxtls OR tlsasx) OR (telstra AND (stock OR shares OR trading OR invest OR market OR network OR company)) OR (telstra AND (connectivity OR speed)) OR (telstra AND (downward OR upward OR trend OR coverage)) OR (telstra AND (outage OR bandwith OR service)) OR (telstra AND (pldt OR iinet OR telecom OR vodafone OR optus OR competitor)) OR (telstra AND (broadband OR 5G)) OR (telstra AND (nsw OR australia OR australian))'
    #Second set of keywords for Telstra
    #c.Search = '(telstra AND (4G OR internet OR customer OR business OR mbps OR connection OR telecommunication OR covid OR corona OR coronavirus OR pandemic))'
    #First set of keywords for Qantas
    #c.Search = '(Qantas AND (platinum OR credits OR promotion OR gold OR flyer OR frequent OR flight OR biofuel OR aviation OR plane OR pilot OR co-pilot OR australia OR delay OR international OR routes OR roundtrip OR cancel))'
    #Second set of keywords for Qantas
    c.Search = '(qantas AND (airline OR time OR boeing OR passenger OR airport OR covid OR service OR aircraft OR coronavirus OR commercial OR domestic OR economy)) OR (ASX AND QAN) OR (asxqan OR qanasx) OR (qantas AND (stock OR shares OR trading OR invest OR market OR company OR pandemic OR corona OR outbreak))'
    # Custom output format
    c.Format = "Username: {username} |  Tweet: {tweet}"##Specifying the format in which the results of tweets fetched si to be displayed
    c.Limit = 10000#number of tweets to pull
    c.Pandas = True
    c.Pandas_clean = True
    c.Lang = 'en'
    c.Hide_output = True
    c.Count = True
    c.Popular_tweets = True#to scrap only popular tweets of users
    c.Since = datetime.strftime(start_date, format='%Y-%m-%d')##Setting up the start date
    c.Until = datetime.strftime(end_date, format='%Y-%m-%d')##Setting up the end date
    ###tweet filtering based on likes, replies and retweets can change the minimum categories but as we are fetching tweets of normal users
    ###and so the criteria iskept low so that more tweets can be fetched
    c.Min_likes = 20
    c.Min_replies = 3
    c.Min_retweets = 2
    twint.run.Search(c)##Search for tweets based on the above configuration
    try:
        return twint.output.panda.Tweets_df[columns]###Convert the twint returned results into a dataframe with only the columns mentioned
    except:
        return False##If no tweets are fetched then it returns false specifying that next operations must not be performed


''' Method to perform Natural language Processing operations on the tweets such as removing stopwords, lowercase each letter, remove
punctuation, rmeove urls, remove repeating characters, stemming, lematization, remove twitter handles and so on'''
def data_cleaner(tweet):
    stopwordlist = ['a', 'about', 'above', 'after', 'again', 'ain', 'all', 'am', 'an','and','any','are', 'as', 'at', 'be', 'because', 'been', 'before','being', 'below', 'between','both', 'by', 'can', 'd', 'did', 'do','does', 'doing', 'down', 'during', 'each','few', 'for', 'from','further', 'had', 'has', 'have', 'having', 'he', 'her', 'here','hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in','into','is', 'it', 'its', 'itself', 'just', 'll', 'm', 'ma','me', 'more', 'most','my', 'myself', 'now', 'o', 'of', 'on', 'once','only', 'or', 'other', 'our', 'ours','ourselves', 'out', 'own', 're','s', 'same', 'she', "shes", 'should', "shouldve",'so', 'some', 'such','t', 'than', 'that', "thatll", 'the', 'their', 'theirs', 'them','themselves', 'then', 'there', 'these', 'they', 'this', 'those','through', 'to', 'too','under', 'until', 'up', 've', 'very', 'was','we', 'were', 'what', 'when', 'where','which','while', 'who', 'whom','why', 'will', 'with', 'won', 'y', 'you', "youd","youll", "youre","youve", 'your', 'yours', 'yourself', 'yourselves']
    tweet['original'] = tweet['text']###Adding another column to the dataframe saving the original tweets
    tweet['text']=tweet['text'].str.lower()###Lowercase the tweets
    ###Clearing the stop words from the tweets
    STOPWORDS = set(stopwordlist)
    def cleaning_stopwords(text):
        return " ".join([word for word in str(text).split() if word not in STOPWORDS])
    tweet['text'] = tweet['text'].apply(lambda text: cleaning_stopwords(text))##For each tweets in the columns clear the stopwords
    ###Clearing twitter handles @user by finding the pattern and then removing the text from the tweet
    def clearing_twitter_handles(text, pattern):
        r = re.findall(pattern, text)
        for i in r:
            text = re.sub(i,'',text)
        return text
    tweet['text']= tweet['text'].apply(lambda x: clearing_twitter_handles(x,"@[\w]*"))##For each tweets in the columns clear the twitter handles
    def cleaning_URLs(data):
        return re.sub('((www.[^s]+)|(https://[^s]+))',' ',data)
    tweet['text'] = tweet['text'].apply(lambda x: cleaning_URLs(x))##For each tweets in the columns clear the urls
    ###Clearing punctuations from the tweets
    punctuations_list = string.punctuation
    def cleaning_punctuations(text):
        translator = str.maketrans('', '', punctuations_list)
        return text.translate(translator)
    tweet['text']= tweet['text'].apply(lambda x: cleaning_punctuations(x))##For each tweets in the columns clear the punctuations
    ###Removing repeating characters
    #try to remove repeating characters though this may always not be useful, if a character is repeated more than twice then reduce the character
    #reason for performing this is because in tweets people can express themselves in different ways such as 'hapyyyyy'
    def cleaning_repeating_char(text):
        return re.sub(r'(.)2+', r'2', text)
    tweet['text'] = tweet['text'].apply(lambda x: cleaning_repeating_char(x))##For each tweets in the columns reduce the repeating characters
    ###Remove urls
    ###Cleaning numbers
    def cleaning_numbers(data):
        return re.sub('[0-9]+', '', data)
    tweet['text'] = tweet['text'].apply(lambda x: cleaning_numbers(x))##For each tweets in the columns clear the numbers
    ###Removing special characters, numbers and punctuations
    tweet['text'] = tweet['text'].apply(lambda x: x.replace("[^a-zA-Z#]", " "))
    ###Removing short words, words less than size 3 will be removed
    tweet['text'] = tweet['text'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>3]))
    ###Tokenizing
    tweet['text'] = tweet['text'].apply(lambda x:re.split('\W+', x))###Seperate the words into lists or tokenize the sentence
    ###Stemming can be applied but is not applied as some words are losing meaning and can cause the sentiment analyzer to not recognize the words  
    ###Lemmatizer can be appled but is not applied as some words being formed is improper leading to the possibilty that the sentiment analyzer may misbehave
    tweet['text'] = tweet['text'].apply(lambda x:' '.join(x))###Combine the tokenized words
    return tweet###Return the tweets after being pre-processed

''' Method to save the fetched tweets into an excel sheet with the relevant data in specific columns'''
def save_preprocessed_tweets_to_spreadsheet(tweets,worksheet,count):##Paremeters are the tweets, the worksheet in which to save and row count
    try:
        for index, each_tweet in tweets.iterrows():###ietarte through all the twitter tweets
            cell1 = 'A'+str(count)
            cell2 = 'B'+str(count)
            cell3 = 'C'+str(count)
            cell4 = 'D'+str(count)
            cell5 = 'E'+str(count)
            cell6 = 'F'+str(count)
            if each_tweet.english>0.1:###Check if there is some english percentage in the tweets so that other language tweets are not added
                worksheet.write(str(cell1), str(each_tweet.date))##Save the date
                worksheet.write(str(cell2), each_tweet.username)##Save the username
                worksheet.write(str(cell3), each_tweet.text)##Save the nlp preprocessed tweet
                worksheet.write(str(cell4), each_tweet.original)##Save the original tweet
                worksheet.write(str(cell5), each_tweet.nlikes)##Save the number of liked in the tweet
                worksheet.write(str(cell6), each_tweet.english)##Save the english percentage in te tweet
                count=count+1###Increase the row count
        return worksheet,count###Returnt the current excel worksheet and the row count
    except:
        print("Error occured")


''' Method to check if the tweets consists of english words and the percentage of wnglish words
Nouns such as telstra and quantas will not be in dictionary and so the english percentage can reduce
'''
def english_chekcer_in_tweets(tweet):
    d = enchant.Dict("en_AU")##Setting the dictionary to be australian
    def check_if_most_words_are_english(text):
        words_list = text.split()###Split the text into words
        total_words = len(words_list)###Count the total number of words
        english_words = 0
        for w in words_list:
            if (d.check(w)):###returns true if the word is english
                english_words = english_words+1##Increment the count of english words
        if total_words==0:
            return float(0)
        else:
            return (float(english_words)/float(total_words))##Count the total percentage of wnglish words
    tweet['english'] = tweet['text'].apply(lambda x: check_if_most_words_are_english(x))###Checking each row tweets and assigning english percentage
    return tweet###Return the twitter dataframe with the new column
    


if __name__ == "__main__":
    ###Setting up the initial dates for twitter fetch
    ###keeping the start date as 2017-12-28 as some past tweets will help determine the sentiment for 01/01/2018
    initial_year = 2018
    initial_month = 1
    company_name='Qantas'
    search_category_1=True##Search catefory 1 indicates tweets based on the the first set of keywords is being generated
    columns = ["date", "username", "tweet", "hashtags", "nlikes"]
    filename = 'Twitter_dataset_obtained_from_twint/twitter_tweets_dataset_Qantas_2018_04_06.xlsx'
    workbook = xlsxwriter.Workbook(filename)###Setting up one excelsheet
    worksheet = workbook.add_worksheet()
    count=1
    tweets = twint_configuration_and_search(date(2018, 3, 30),date(2018, 6, 30),columns)
    if isinstance(tweets,pd.DataFrame):##Check if the pandas dataframe was created
        tweets = tweets.rename(columns={'tweet': 'text'})###Renaming one column
        tweets = data_cleaner(tweets)###Perform pre-processing on the tweets
        tweets = english_chekcer_in_tweets(tweets)###Checking english percentage
        worksheet,count=save_preprocessed_tweets_to_spreadsheet(tweets,worksheet,count)
    workbook.close()
    ###Search category 2 indicates tweets based on the second set of keywords is being generated
    ###The below chunk code is able to fetch tweets automatically based on date and months but due to the limitation of twint to fetch tweets at a single request the below code is commented and the data is collected manually by changing dates keeping the limitation in consideration
    '''while initial_year!=2019:##Iterate until the year 2021 is reached
        filename = 'Twitter_dataset_obtained_from_twint/twitter_tweets_dataset_'+company_name+str(initial_year)+'_'+str(initial_month)+'.xlsx'
        workbook = xlsxwriter.Workbook(filename)###Setting up one excelsheet
        ###Must change the name on a monthly basis
        worksheet = workbook.add_worksheet()
        count=1
        if initial_month==2:
            if initial_year%4==0:
                tweets = twint_configuration_and_search(date(initial_year, initial_month-1, 27),date(initial_year, initial_month, 29),columns)#'2019-10-28','2019-11-30',query)
                #print(twint.output)
                #print(twint.output.panda.Tweets_df.columns)###Print all the available columns
                if isinstance(tweets,pd.DataFrame):##Check if the pandas dataframe was created
                    tweets = tweets.rename(columns={'tweet': 'text'})###Renaming one column
                    tweets = data_cleaner(tweets)###Perform pre-processing on the tweets
                    tweets = english_chekcer_in_tweets(tweets)###Checking english percentage
                    worksheet,count=save_preprocessed_tweets_to_spreadsheet(tweets,worksheet,count)
            else:
                tweets = twint_configuration_and_search(date(initial_year, initial_month-1, 27),date(initial_year, initial_month, 28),columns)
                if isinstance(tweets,pd.DataFrame):##Check if the pandas dataframe was created
                    tweets = tweets.rename(columns={'tweet': 'text'})###Renaming one column
                    tweets = data_cleaner(tweets)###Perform pre-processing on the tweets
                    tweets = english_chekcer_in_tweets(tweets)###Checking english percentage
                    #print(tweets)
                    worksheet,count=save_preprocessed_tweets_to_spreadsheet(tweets,worksheet,count)
        else:
            if ((initial_month==3)or(initial_month==5)or(initial_month==7)or(initial_month==8)or(initial_month==10)or(initial_month==12)):
                tweets = twint_configuration_and_search(date(initial_year, initial_month-1, 27),date(initial_year, initial_month, 31),columns)
                if isinstance(tweets,pd.DataFrame):##Check if the pandas dataframe was created
                    tweets = tweets.rename(columns={'tweet': 'text'})###Renaming one column
                    tweets = data_cleaner(tweets)###Perform pre-processing on the tweets
                    tweets = english_chekcer_in_tweets(tweets)###Checking english percentage
                    #print(tweets)
                    worksheet,count=save_preprocessed_tweets_to_spreadsheet(tweets,worksheet,count)
            elif initial_month==1:
                tweets = twint_configuration_and_search(date(initial_year-1, 12, 27),date(initial_year, initial_month, 31),columns)
                if isinstance(tweets,pd.DataFrame):##Check if the pandas dataframe was created
                    tweets = tweets.rename(columns={'tweet': 'text'})###Renaming one column
                    tweets = data_cleaner(tweets)###Perform pre-processing on the tweets
                    tweets = english_chekcer_in_tweets(tweets)###Checking english percentage
                    #print(tweets)
                    worksheet,count=save_preprocessed_tweets_to_spreadsheet(tweets,worksheet,count)
            else:
                tweets = twint_configuration_and_search(date(initial_year, initial_month-1, 27),date(initial_year, initial_month, 30),columns)
                if isinstance(tweets,pd.DataFrame):##Check if the pandas dataframe was created
                    tweets = tweets.rename(columns={'tweet': 'text'})###Renaming one column
                    tweets = data_cleaner(tweets)###Perform pre-processing on the tweets
                    tweets = english_chekcer_in_tweets(tweets)###Checking english percentage
                    #print(tweets)
                    worksheet,count=save_preprocessed_tweets_to_spreadsheet(tweets,worksheet,count)
        if initial_month==12:###If december data if fetched then must start with january of next year
            initial_year=initial_year+1
            initial_month=1
        else:###Else keep incrementing the month by keeping the year fixed
            initial_month = initial_month+1
        workbook.close()###Close the workbook and save the result
        sleep(10)'''