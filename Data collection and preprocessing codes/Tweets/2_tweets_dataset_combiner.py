'''This python file consists of code to read all the tweets excelsheet gathered after executing python file 'twitter_tweets_dataset_collector.py'
the excelsheets must be combined into a single file and then the sentiments must be determined on a day to day basis'''
###This python code is only to reverse the order of data in the excelsheet and save all in one
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

'''Section 1: This is to read all the excel files in the folder and combine all and also remove duplicated tweets 
as some tweets could have been fetched multiple times
calculate sentiment and polarity and store
all into one file back again'''

folder_path = 'Twitter_dataset_obtained_from_twint/Qantas_fetched_tweets'##the folder in which all the excel sheets are present
original_dataframe_of_tweets = 0
changed = 0
filtered_words = ""
actual_words=""

#Method to determine the sentiment of a tweet using textblob sentiment analyzer, the method returns positive or negative sentiment 
#and also the polarity value
def determine_sentiment_from_tweet(each_tweet_text):#Using textblob's method determine/classify the sentiment
    analysis_result = TextBlob(each_tweet_text)
    #Determining the sentiment polarity
    if analysis_result.polarity>0:
      return 'positive',analysis_result.polarity
    elif analysis_result.polarity==0:
      return 'neutral',analysis_result.polarity
    else:
      return 'negative',analysis_result.polarity

###Iterate through all the files present in that folder
for filename in glob.glob(os.path.join(folder_path, '*.xlsx')):
    with open(filename, 'r') as f:##Open an excel file
        print(filename)
        filename = filename.split('\\')
        filename = filename[1]
        filepath = folder_path+'/'+filename
        print(filepath)
        tweets_headlines = pd.read_excel(filepath, index_col=0,header=None)###Read the excel file
        #print(news_headlines.head())
        tweets_headlines = tweets_headlines.reset_index()
        tweets_headlines.columns = ['DateTime','Username','tweet','original_tweet','nlikes','english_perct']###assign the particular columns to the read data
        tweets_headlines = tweets_headlines.iloc[::-1]###Reverse the dataframe because the tweets are fetched in a reverse way
        #for index, tweets in tweets_headlines.iterrows():
        #    print (tweets)
        if changed==0:
            original_dataframe_of_tweets = tweets_headlines
            changed=1
        else:
            print(tweets_headlines)
            original_dataframe_of_tweets = original_dataframe_of_tweets.append(tweets_headlines,ignore_index=True)###append all the tweets into a single dataframe
            print(original_dataframe_of_tweets)
            #original_dataframe_of_tweets = original_dataframe_of_tweets.reset_index()
print("Length after combining all")
print(len(original_dataframe_of_tweets))##Print the length after having combined all the tweets
#print(original_dataframe_of_tweets)
###Remove the duplicates rows from the tweets
original_dataframe_of_tweets.drop_duplicates(subset=['DateTime','Username','tweet','original_tweet','nlikes','english_perct'],keep='first',inplace=True)
print("Length after combining all")
print(len(original_dataframe_of_tweets))
#print(original_dataframe_of_tweets)
n=50

###This section is to provide analysis of the users with most tweets and the most common words as that could help to generate more
###keywords
print(original_dataframe_of_tweets['Username'].value_counts()[:n])###check the usernames with the most tweets and so the usernames are counted
###Checking the most common occured words
filtered_words = "".join(original_dataframe_of_tweets['tweet']).split()##combining all the words present in the column filtered words
actual_words="".join(original_dataframe_of_tweets['original_tweet']).split()##combining all the original tweets
print(Counter(filtered_words).most_common(200))###find the most common words in the filtered tweets dataset

original_dataframe_of_tweets['DateTime'] = pd.to_datetime(original_dataframe_of_tweets['DateTime'],format='%Y-%m-%d %H:%M:%S')
original_dataframe_of_tweets = original_dataframe_of_tweets.sort_values(by="DateTime")
#original_dataframe_of_tweets['DateTime'] = datetime.strftime(original_dataframe_of_tweets['DateTime'], format='%Y-%m-%d %H:%M:%S')

###Code to write everything to excelsheet as now the duplicate tweets had been removed
workbook = xlsxwriter.Workbook('Twitter_dataset_obtained_from_twint/final_tweet_Qantas_dataset_with_sentiments.xlsx')
worksheet = workbook.add_worksheet()
count=1
nltksentimenet_analyzer = SentimentIntensityAnalyzer()###setting up the ntlk sentiment analyzer
for index, each_tweet in original_dataframe_of_tweets.iterrows():
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
    cell10 = 'J'+str(count)
    cell11 = 'K'+str(count)
    cell12 = 'L'+str(count)
    cell13 = 'M'+str(count)
    sentiment1,polarity1 = determine_sentiment_from_tweet(each_tweet.tweet)##generating the textblob sentiment and polarity for filtered tweet
    sentiment2,polarity2 = determine_sentiment_from_tweet(each_tweet.original_tweet)##generating the textblob sentiment and polarity for original tweet
    worksheet.write(str(cell1), str(each_tweet.DateTime))###write the date in col1
    worksheet.write(str(cell2), each_tweet.Username)###write the username in col2
    worksheet.write(str(cell3), each_tweet.tweet)##write the filtered tweet in col3
    worksheet.write(str(cell4), each_tweet.original_tweet)##write the original tweet in col4
    worksheet.write(str(cell5), each_tweet.nlikes)##write the number of likes in col5
    worksheet.write(str(cell6), each_tweet.english_perct)###write the english percentage value in col6
    ###Textblob sentiments
    worksheet.write(str(cell7), sentiment1)##Sentiment of the filtered words using textblob in col7
    worksheet.write(str(cell8), polarity1)##Polarity of the filtered words using textblob in col8
    worksheet.write(str(cell9), sentiment2)##Sentiment on the original words using textblob in col9
    worksheet.write(str(cell10), polarity2)##Polarity of the filtered words using textblob in col10
    ###ntlk library sentiments
    nltksentimenet_analyzer
    dict_tweet = nltksentimenet_analyzer.polarity_scores(each_tweet.tweet) 
    worksheet.write(str(cell11), dict_tweet['compound'])##Polarity of the filtered tweet by ntlk in col11
    dict_original_tweet = nltksentimenet_analyzer.polarity_scores(each_tweet.original_tweet)
    worksheet.write(str(cell12), dict_original_tweet['compound'])##Polarity of the original tweet by ntlk in col12
    ###Average of all polarity values of sentiments in col13
    worksheet.write(str(cell13), float((polarity1+polarity2+dict_tweet['compound']+dict_original_tweet['compound'])/4))
    count=count+1
workbook.close()