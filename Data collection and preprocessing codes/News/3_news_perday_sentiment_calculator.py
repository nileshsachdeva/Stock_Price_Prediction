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

'''Section3: Now the previous excelsheet has the sentiments and so now time to combine the sentiments based on the date'''
news_headlines = pd.read_excel('News_dataset_obtained_manually/qantas_final_news_dataset_extracted_manually_v2.xlsx', index_col=0,header=None)
news_headlines = news_headlines.reset_index()
news_headlines.columns = ['Date','Headline','filtered_headline','Source','polarity1','polarity2','polarity3','polarity4','avg_polarity']
news_headlines['Date'] = pd.to_datetime(news_headlines['Date'],format='%Y-%m-%d %H:%M:%S')
print(news_headlines.head())

one_day_sentiment = {"date":[],"avg_sentiment":[],"avg_pol1":[],"avg_pol2":[],"avg_pol3":[],"avg_pol4":[],"count":[]}
current_date=0
average_sentiment=0#variable to keep track of the average sentiment for the day
average_polarity1=0#variable to keep track of the average polarity1 for the day
average_polarity2=0#variable to keep track of the average polarity2 for the day
average_polarity3=0#variable to keep track of the average polarity3 for the day
average_polarity4=0#variable to keep track of the average polarity4 for the day
count=0

for index, each_row in news_headlines.iterrows():##Iterating through each and every news data
    if current_date==0:##The first row and so assign the variables with the data in the row
        current_date=each_row.Date.date()##Save the current iterating date in the variable
        average_sentiment = each_row.avg_polarity
        average_polarity1 = each_row.polarity1
        average_polarity2 = each_row.polarity2
        average_polarity3 = each_row.polarity3
        average_polarity4 = each_row.polarity4
        count=1
    elif current_date!=each_row.Date.date():##If there is a change in the date then the previous date averaged sentiments must be saved
        average_sentiment = float(average_sentiment)/float(count)
        average_polarity1 = float(average_polarity1)/float(count)
        average_polarity2 = float(average_polarity2)/float(count)
        average_polarity3 = float(average_polarity3)/float(count)
        average_polarity4 = float(average_polarity4)/float(count)
        one_day_sentiment["date"].append(current_date)
        one_day_sentiment["avg_sentiment"].append(average_sentiment)
        one_day_sentiment["avg_pol1"].append(average_polarity1)
        one_day_sentiment["avg_pol2"].append(average_polarity2)
        one_day_sentiment["avg_pol3"].append(average_polarity3)
        one_day_sentiment["avg_pol4"].append(average_polarity4)
        one_day_sentiment["count"].append(count)
        current_date=each_row.Date.date()
        check=0
        average_sentiment = each_row.avg_polarity
        average_polarity1 = each_row.polarity1
        average_polarity2 = each_row.polarity2
        average_polarity3 = each_row.polarity3
        average_polarity4 = each_row.polarity4
        count=1
    elif current_date==each_row.Date.date():##If the same day has more news headlines then the sentiments needs to be averaged
        ###Add the sentiment value for the same day
        average_sentiment = average_sentiment + each_row.avg_polarity
        average_polarity1 = average_polarity1+each_row.polarity1
        average_polarity2 = average_polarity2+each_row.polarity2
        average_polarity3 = average_polarity3+each_row.polarity3
        average_polarity4 = average_polarity4+each_row.polarity4
        count=count+1
one_day_news_sentiments_df = pd.DataFrame.from_dict(one_day_sentiment)
print(one_day_news_sentiments_df.head(60))

'''
#Need to do average of sentiments based on the date
#but unlike tweets here everyday there is no news headlines so
#only if there is past day sentiment then average it else just consider one day's sentiment
'''
one_day_news_sentiments_df['two_day_news'] = one_day_news_sentiments_df.apply(lambda row: row.avg_sentiment, axis=1)
for i in range(1,len(one_day_news_sentiments_df)):
    today = one_day_news_sentiments_df.loc[i,'date']##get the current date being iterated
    yesterday = today - timedelta(days=1)##get the previous date
    #print(str(today)+" "+str(yesterday))
    ##if the previous date data/sentiment is present then average it else just consider the data of current date
    if i==0:##If the first row is being iterated then its obvious that past date headline is not present, so just store the same value
        one_day_news_sentiments_df.loc[i,'two_day_news'] = (0+one_day_news_sentiments_df.loc[i,'two_day_news'])
    elif one_day_news_sentiments_df.loc[i-1,'date']==yesterday:#check if the current date has a previous date sentiment
        one_day_news_sentiments_df.loc[i,'two_day_news'] = (one_day_news_sentiments_df.loc[i-1,'two_day_news'] + one_day_news_sentiments_df.loc[i,'avg_sentiment'])/2
    else:
        one_day_news_sentiments_df.loc[i,'two_day_news'] = one_day_news_sentiments_df.loc[i,'avg_sentiment']

print(one_day_news_sentiments_df)
    
workbook = xlsxwriter.Workbook('News_dataset_obtained_manually/qantas_final_news_dataset_extracted_manually_v3.xlsx')
worksheet = workbook.add_worksheet()
count=1
for index, each_news in one_day_news_sentiments_df.iterrows():
    #tweets[col].apply(lambda x:print(x))
    cell1 = 'A'+str(count)
    cell2 = 'B'+str(count)
    cell3 = 'C'+str(count)
    cell4 = 'D'+str(count)
    cell5 = 'E'+str(count)
    cell6 = 'F'+str(count)
    cell7 = 'G'+str(count)
    worksheet.write(str(cell1), str(each_news.date))
    worksheet.write(str(cell2), each_news.avg_sentiment)
    worksheet.write(str(cell3), each_news.avg_pol1)
    worksheet.write(str(cell4), each_news.avg_pol2)
    worksheet.write(str(cell5), each_news.avg_pol3)##Sentiment of the filtered headline using textblob
    worksheet.write(str(cell6), each_news.avg_pol4)##Sentiment on the original headline using textblob
    worksheet.write(str(cell7), each_news.two_day_news)##Polarity of the original tweet by ntlk
    ###Average of all
    count=count+1
workbook.close()