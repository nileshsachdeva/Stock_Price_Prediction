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

'''Section1: code to read the manually combines excelsheet for news headlines 
and sort the data based on date and write it to another new excel sheet'''

manual_news_headlines = pd.read_excel('News_dataset_obtained_manually/Qantas_final_news_dataset_extracted_manually.xlsx', index_col=0,header=0)##Read the excelsheet data into a python dataframe
#print(manual_news_headlines)
manual_news_headlines = manual_news_headlines.reset_index()##Reset the indexes as the excel sheet index some columns could have been deleted/removed also
manual_news_headlines.columns = ['Date','Headline','Source']##Assign headlines to the dataframe
#print(manual_news_headlines.head())
manual_news_headlines['Date'] = pd.to_datetime(manual_news_headlines['Date'],format='%Y-%m-%d')#Convert the date object into a datetime object
#print(manual_news_headlines['Date'].head(500))
manual_news_headlines = manual_news_headlines.sort_values(by="Date")#Sorting the dataframe based on the date of the news published
manual_news_headlines = manual_news_headlines.reset_index()##Again resetting the index as data could have been shuffled
print(manual_news_headlines['Date'].head(1200))

workbook1 = xlsxwriter.Workbook('News_dataset_obtained_manually/qantas_final_news_dataset_extracted_manually_v1.xlsx')
worksheet1 = workbook1.add_worksheet()
count=1
for index, each_day in manual_news_headlines.iterrows():
    cell1 = 'A'+str(count)
    cell2 = 'B'+str(count)
    cell3 = 'C'+str(count)
    worksheet1.write(str(cell1), str(each_day.Date))##Col1 date
    worksheet1.write(str(cell2), each_day.Headline)##Col2 average sentiment
    worksheet1.write(str(cell3), each_day.Source)##Col3 two day sentiment
    count=count+1
workbook1.close()