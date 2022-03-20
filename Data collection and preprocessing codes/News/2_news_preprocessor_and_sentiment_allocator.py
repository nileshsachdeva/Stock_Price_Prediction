''' Python code to read the manually extracted news headlines and sort them accordingly and allocate sentiments to the headlines on a day to day basis'''
###Import the necessary modules required for the code

import os,glob
import pandas as pd
from collections import Counter
import xlsxwriter
from textblob import TextBlob
import spacy
import nltk
import matplotlib.pyplot as plt
#nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import datetime, timedelta

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
#nltk.download('stopwords')
#nltk.download('wordnet')
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
import string
import seaborn as sns
import itertools
import collections
import datetime
import twint
import nest_asyncio

from wordcloud import WordCloud, STOPWORDS
from PIL import Image
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import SnowballStemmer, PorterStemmer, WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import pos_tag
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import json
import xlsxwriter
from datetime import datetime, timedelta

#SPACY
import spacy
import textacy
import string

from time import sleep

import enchant


'''Section2: read the above created excelsheet and determine sentiments for each news headline and store them into another excelsheet'''
news_headlines = pd.read_excel('News_dataset_obtained_manually/qantas_final_news_dataset_extracted_manually_v1.xlsx', index_col=0,header=None)
news_headlines = news_headlines.reset_index()
news_headlines.columns = ['Date','Headline','Source']
news_headlines['Date'] = pd.to_datetime(news_headlines['Date'],format='%Y-%m-%d %H:%M:%S')
print(news_headlines.head())

def data_cleaner(news):
    stopwordlist = ['a', 'about', 'above', 'after', 'again', 'ain', 'all', 'am', 'an','and','any','are', 'as', 'at', 'be', 'because', 'been', 'before','being', 'below', 'between','both', 'by', 'can', 'd', 'did', 'do','does', 'doing', 'down', 'during', 'each','few', 'for', 'from','further', 'had', 'has', 'have', 'having', 'he', 'her', 'here','hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in','into','is', 'it', 'its', 'itself', 'just', 'll', 'm', 'ma','me', 'more', 'most','my', 'myself', 'now', 'o', 'of', 'on', 'once','only', 'or', 'other', 'our', 'ours','ourselves', 'out', 'own', 're','s', 'same', 'she', "shes", 'should', "shouldve",'so', 'some', 'such','t', 'than', 'that', "thatll", 'the', 'their', 'theirs', 'them','themselves', 'then', 'there', 'these', 'they', 'this', 'those','through', 'to', 'too','under', 'until', 'up', 've', 'very', 'was','we', 'were', 'what', 'when', 'where','which','while', 'who', 'whom','why', 'will', 'with', 'won', 'y', 'you', "youd","youll", "youre","youve", 'your', 'yours', 'yourself', 'yourselves']
    ###Lowercase the tweets
    news['filtered_headline'] = news['Headline']
    news['filtered_headline']=news['filtered_headline'].str.lower()
    ###Clearing the stop words from the tweets
    STOPWORDS = set(stopwordlist)
    def cleaning_stopwords(text):
        return " ".join([word for word in str(text).split() if word not in STOPWORDS])
    news['filtered_headline'] = news['filtered_headline'].apply(lambda text: cleaning_stopwords(text))
    english_punctuations = string.punctuation
    punctuations_list = english_punctuations
    ###Clearing twitter handles @user
    #def clearing_twitter_handles(text, pattern):
    #    r = re.findall(pattern, text)
    #    for i in r:
    #        text = re.sub(i,'',text)
    #    return text
    #news['filtered_headline']= news['filtered_headline'].apply(lambda x: clearing_twitter_handles(x,"@[\w]*"))
    ###Remove urls
    def cleaning_URLs(data):
        return re.sub('((www.[^s]+)|(https://[^s]+))',' ',data)
    news['filtered_headline'] = news['filtered_headline'].apply(lambda x: cleaning_URLs(x))
    ###Clearing punctuations
    def cleaning_punctuations(text):
        translator = str.maketrans('', '', punctuations_list)
        return text.translate(translator)
    news['filtered_headline']= news['filtered_headline'].apply(lambda x: cleaning_punctuations(x))
    ###Removing repeating characters
    #try to remove repeating characters though this may always not be useful
    #def cleaning_repeating_char(text):
    #    return re.sub(r'(.)2+', r'2', text)
    #news['filtered_headline'] = news['filtered_headline'].apply(lambda x: cleaning_repeating_char(x))
    ###Cleaning numbers
    def cleaning_numbers(data):
        return re.sub('[0-9]+', '', data)
    news['filtered_headline'] = news['filtered_headline'].apply(lambda x: cleaning_numbers(x))
    ###Removing special characters, numbers and punctuations
    news['filtered_headline'] = news['filtered_headline'].apply(lambda x: x.replace("[^a-zA-Z#]", " "))
    ###Removing short words, words less than size 3 will be removed
    news['filtered_headline'] = news['filtered_headline'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>3]))
    ###Tokenizing
    #from nltk.tokenize import RegexpTokenizer
    #tokenizer = RegexpTokenizer(r'w+')
    #tweet['text'] = tweet['text'].apply(tokenizer.tokenize)
    news['filtered_headline'] = news['filtered_headline'].apply(lambda x:re.split('\W+', x))
    #applying stemming
    ###Stemming
    st = nltk.PorterStemmer()
    ###can use Snowball Stemmer as that is like Porter2 and a better version
    def stemming_on_text(data):
        data = [st.stem(word) for word in data]
        return data
    #news['filtered_headline']= news['filtered_headline'].apply(lambda x: stemming_on_text(x))
    
    ###Lemmatizer
    lm = nltk.WordNetLemmatizer()
    def lemmatizer_on_text(data):
        text = [lm.lemmatize(word) for word in data]
        return data
    #news['filtered_headline'] = news['filtered_headline'].apply(lambda x: lemmatizer_on_text(x))
    
    news['filtered_headline'] = news['filtered_headline'].apply(lambda x:' '.join(x))
    return news

def determine_sentiment_from_tweet(headline):#Using textblob's method determine/classify the sentiment
    analysis_result = TextBlob(headline)
    #Determining the sentiment polarity
    return analysis_result.polarity

news_headlines=data_cleaner(news_headlines)###Add another column where the news headlines are filtered
print(news_headlines)

###Code to write everything to excelsheet
workbook = xlsxwriter.Workbook('News_dataset_obtained_manually/final_news_dataset_extracted_manually_v2.xlsx')
worksheet = workbook.add_worksheet()
count=1
nltksentimenet_analyzer = SentimentIntensityAnalyzer()
for index, each_news in news_headlines.iterrows():
    #tweets[col].apply(lambda x:print(x))
    cell1 = 'A'+str(count)
    cell2 = 'B'+str(count)
    cell3 = 'C'+str(count)
    cell4 = 'D'+str(count)
    cell5 = 'E'+str(count)
    cell6 = 'F'+str(count)
    cell7 = 'G'+str(count)
    cell8 = 'H'+str(count)
    cell9 = 'I'+str(count)
    polarity1 = determine_sentiment_from_tweet(each_news.filtered_headline)
    polarity2 = determine_sentiment_from_tweet(each_news.Headline)
    worksheet.write(str(cell1), str(each_news.Date))
    worksheet.write(str(cell2), each_news.Headline)
    worksheet.write(str(cell3), each_news.filtered_headline)
    worksheet.write(str(cell4), each_news.Source)
    ###Textblob sentiments
    worksheet.write(str(cell5), polarity1)##Sentiment of the filtered headline using textblob
    worksheet.write(str(cell6), polarity2)##Sentiment on the original headline using textblob
    ###ntlk library sentiments
    dict_news = nltksentimenet_analyzer.polarity_scores(each_news.filtered_headline)
    worksheet.write(str(cell7), dict_news['compound'])##Polarity of the filtered headline by ntlk
    dict_original_news = nltksentimenet_analyzer.polarity_scores(each_news.Headline)
    worksheet.write(str(cell8), dict_original_news['compound'])##Polarity of the original tweet by ntlk
    ###Average of all
    worksheet.write(str(cell9), float((polarity1+polarity2+dict_news['compound']+dict_original_news['compound'])/4))
    count=count+1
workbook.close()