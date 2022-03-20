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

'''Section 2: This section is to be executed after section1 is completed and comment the code of section1.
Open the combined file, and now sentiment of each day is determined by average of sentiments of each day.
Sentiment of two-days, i.e. affect of yesterday's sentiments on today's sentiments is calculated.
The usernames who had tweeted the most weights are added to their tweet sentiments.
Sentiment of three-days,i.e. affect of previous two days is computed.
The data of weekends is also dealt as monday has impact for data of friday, saturday and sunday.
    tuesday has impact for data on saturday, sunday and monday.
 Plot the graph of sentiment values to check if the trend is the same as historical data'''

tweets_headlines = pd.read_excel('Twitter_dataset_obtained_from_twint/final_tweet_Qantas_dataset_with_sentiments.xlsx', index_col=0,header=None)###The excel file created in section1 is being read
tweets_headlines = tweets_headlines.reset_index()
tweets_headlines.columns = ['DateTime','Username','tweet','original_tweet','nlikes','english_perct','sentiment1','polarity1','sentiment2','polarity2','polarity3','polarity4','avg_polarity']##Assign column names to the dataframe
tweets_headlines['DateTime'] = pd.to_datetime(tweets_headlines['DateTime'],format='%Y-%m-%d %H:%M:%S')
print(tweets_headlines.head())
#n=50
###uncomment to check the users with most tweets again
#print(tweets_headlines['Username'].value_counts()[:n])
##Assigning priority to the tweets of users who have most tweets, considering that tweets from them have more impact on the users
###For telstra
#top_tweet_usernames = [{'username':'Telstra','weight':1.5},{'username':'Telstra_news','weight':1.4},{'username':'andy_penn','weight':1.3},{'username':'chrismurphys','weight':1.2}]
###For Qantas = 
top_tweet_usernames = [{'username':'Qantas','weight':1.5},{'username':'flightradar24','weight':1.4},{'username':'cnni','weight':1.3},{'username':'Reuters','weight':1.2}]
'''
    One day sentiments
    In this the average of sentiment of all tweets for a day is computed, such as if there are 5 tweets for 01/01/2018 then compute the average of those 5 tweets and mention that as the average sentiment of that day
'''
one_day_sentiment = {"date":[],"avg_sentiment":[],"avg_pol1":[],"avg_pol2":[],"avg_pol3":[],"avg_pol4":[],"count":[]}##Setting up a dictionary for the average daywise sentiments 
current_date=0
average_sentiment=0
average_polarity1=0
average_polarity2=0
average_polarity3=0
average_polarity4=0
count=0
for index, each_row in tweets_headlines.iterrows():###iterate through the dataframe consisting of all the twitter tweets
    if current_date==0:##If the first row is being iterated
        current_date=each_row.DateTime.date()##Save the date
        check=0
        for d in top_tweet_usernames:##Check if the tweet belongs to someone among the top usernames then allocate weights to the values
            if d['username']==each_row.Username:
                average_sentiment = each_row.avg_polarity*d.weight
                average_polarity1 = each_row.polarity1*d['weight']
                average_polarity2 = each_row.polarity2*d['weight']
                average_polarity3 = each_row.polarity3*d['weight']
                average_polarity4 = each_row.polarity4*d['weight']
                check=1
        if check==0:
            average_sentiment = each_row.avg_polarity
            average_polarity1 = each_row.polarity1
            average_polarity2 = each_row.polarity2
            average_polarity3 = each_row.polarity3
            average_polarity4 = each_row.polarity4
        count=1##increase the tweet count to 1
    elif current_date!=each_row.DateTime.date():##Check if there is a mismatch with the current date and the dataframe date being iterated now
        ###if there is a mismatch of date then compute the average 
        average_sentiment = float(average_sentiment)/float(count)
        average_polarity1 = float(average_polarity1)/float(count)
        average_polarity2 = float(average_polarity2)/float(count)
        average_polarity3 = float(average_polarity3)/float(count)
        average_polarity4 = float(average_polarity4)/float(count)
        ###append the data in the dictionary for the previous date
        one_day_sentiment["date"].append(current_date)
        one_day_sentiment["avg_sentiment"].append(average_sentiment)
        one_day_sentiment["avg_pol1"].append(average_polarity1)
        one_day_sentiment["avg_pol2"].append(average_polarity2)
        one_day_sentiment["avg_pol3"].append(average_polarity3)
        one_day_sentiment["avg_pol4"].append(average_polarity4)
        one_day_sentiment["count"].append(count)
        current_date=each_row.DateTime.date()##update the current date variable
        check=0
        for d in top_tweet_usernames:##Again check if the tweet belongs to any of the usernames, if yes then assign weights
            if d['username']==each_row.Username:
                average_sentiment = each_row.avg_polarity*d['weight']
                average_polarity1 = each_row.polarity1*d['weight']
                average_polarity2 = each_row.polarity2*d['weight']
                average_polarity3 = each_row.polarity3*d['weight']
                average_polarity4 = each_row.polarity4*d['weight']
                check=1
        if check==0:###this indicates that the tweet dsnt belongs to the top usernames
            average_sentiment = each_row.avg_polarity
            average_polarity1 = each_row.polarity1
            average_polarity2 = each_row.polarity2
            average_polarity3 = each_row.polarity3
            average_polarity4 = each_row.polarity4
        count=1
    elif current_date==each_row.DateTime.date():##if the current date variable and the tweet date is similar then just add the sentiment values and increase the tweet count for the day
        check=0
        for d in top_tweet_usernames:
            if d['username']==each_row.Username:
                average_sentiment = average_sentiment + each_row.avg_polarity*d['weight']
                average_polarity1 = average_polarity1+each_row.polarity1*d['weight']
                average_polarity2 = average_polarity2+each_row.polarity2*d['weight']
                average_polarity3 = average_polarity3+each_row.polarity3*d['weight']
                average_polarity4 = average_polarity4+each_row.polarity4*d['weight']
                check=1
        if check==0:
            average_sentiment = average_sentiment + each_row.avg_polarity
            average_polarity1 = average_polarity1+each_row.polarity1
            average_polarity2 = average_polarity2+each_row.polarity2
            average_polarity3 = average_polarity3+each_row.polarity3
            average_polarity4 = average_polarity4+each_row.polarity4
        count=count+1##increase count value for the day
    #print("Currentdate:"+str(current_date)+" Row date:"+str(each_row.DateTime.date())+" count:"+str(count))
#print(one_day_sentiment)
one_day_sentiment_df = pd.DataFrame.from_dict(one_day_sentiment)
print(one_day_sentiment_df.head(60))

'''
    Two day sentiment
    The impact of previous day is computed by adding previous day sentiment and today,
    Also the weekenda data is dealt with in this section
'''
print(one_day_sentiment_df.head(30))
one_day_sentiment_df['two_day'] = one_day_sentiment_df.apply(lambda row: row.avg_sentiment, axis=1)###Initially the column average sentiment is duplicated into a new column two day
one_day_sentiment_df['day'] = one_day_sentiment_df.apply(lambda row: row.date.weekday()+1, axis=1)###A new column is added which incides which day of the week that day is such as 1 represents monday and so on till 7 as sunday
for i in range(1,len(one_day_sentiment_df)):
    if i==0:
        one_day_sentiment_df.loc[i,'two_day'] = (0+one_day_sentiment_df.loc[i,'two_day'])##For the first row there is no past data and so the average sentiment is copied for the two day sentiment
    else:
        #Weekend code
        if i>=3:##iterate only if we have atleast 3 records above this record
            ###If its monday, then check if the past dates are sunday, sat and friday if yes then assign weights to those sentiments
            if one_day_sentiment_df.loc[i,'date'].weekday()==0:#if its monday
                #get values of sunday, saturday and friday
                sunday_value=0
                sunday_checker=0
                saturday_value=0
                saturday_checker=0
                friday_value=0
                friday_checker=0
                #Logic is that: 
                #    if monday then check if the values of friday, saturday and sunday exists
                #    if exists then assign weights to them and then add those to the sentiment calculation for monday
                if one_day_sentiment_df.loc[i-1,'date'].weekday()==6:#check if previous row is sunday
                    sunday_value = one_day_sentiment_df.loc[i-1,'two_day']*0.9
                    sunday_checker=1
                if one_day_sentiment_df.loc[i-2,'date'].weekday()==5:#check if previous row is saturday
                    saturday_value=one_day_sentiment_df.loc[i-2,'two_day']*0.8
                    saturday_checker=1
                if one_day_sentiment_df.loc[i-3,'date'].weekday()==4:#check if previous row is friday
                    friday_value = one_day_sentiment_df.loc[i-3,'two_day']*0.7
                    friday_checker=1
                one_day_sentiment_df.loc[i,'two_day'] = (friday_value+saturday_value+sunday_value+one_day_sentiment_df.loc[i,'two_day'])/(friday_checker+saturday_checker+sunday_checker+1)##compute the two day sentiment value by considering weekend data
            ###If its tuesday
            elif one_day_sentiment_df.loc[i,'date'].weekday()==1:#if its tuesday then same logic but not checking monday, sunday and saturday
                #get values of monday, sunday and saturday
                sunday_value3=0
                sunday_checker3=0
                saturday_value3=0
                saturday_checker3=0
                monday_value3=0
                monday_checker3=0
                #Logic is that: 
                #    if tuesday then check if the values of saturday, sunday and monday exists
                #    if exists then assign weights to them and then add those to the sentiment calculation for tuesday
                if one_day_sentiment_df.loc[i-1,'date'].weekday()==0:#previous row is monday
                    monday_value3 = one_day_sentiment_df.loc[i-1,'two_day']*0.9
                    monday_checker3=1
                if one_day_sentiment_df.loc[i-2,'date'].weekday()==6:#previous row is sunday
                    sunday_value3=one_day_sentiment_df.loc[i-2,'two_day']*0.8
                    sunday_checker3=1
                if one_day_sentiment_df.loc[i-3,'date'].weekday()==5:#previous row is friday
                    saturday_value3 = one_day_sentiment_df.loc[i-3,'two_day']*0.7
                    saturday_checker3=1
                one_day_sentiment_df.loc[i,'two_day'] = (monday_value3+saturday_value3+sunday_value3+one_day_sentiment_df.loc[i,'two_day'])/(monday_checker3+saturday_checker3+sunday_checker3+1)
            else:#if its neither monday or tuesday then its weekday and so past date and todays sentiment average is computed
                one_day_sentiment_df.loc[i,'two_day'] = (one_day_sentiment_df.loc[i-1,'two_day']+one_day_sentiment_df.loc[i,'two_day'])/2
        elif i==1:###The same approach but when the second row is being iterated then only check if the previous row is sunday
            if one_day_sentiment_df.loc[i,'date'].weekday()==0:#if its monday
                sunday_value1=0#because only one record is above it
                sunday_checker1=0
                if one_day_sentiment_df.loc[i-1,'date'].weekday()==6:#previous row is sunday
                    sunday_value1 = one_day_sentiment_df.loc[i-1,'two_day']*0.9
                    sunday_checker1=1
                one_day_sentiment_df.loc[i,'two_day'] = (sunday_value1+one_day_sentiment_df.loc[i,'two_day'])/(sunday_checker1+1)
            elif one_day_sentiment_df.loc[i,'date'].weekday()==1:#if its tuesday
                monday_value1=0#because only one record is above it
                monday_checker1=0
                if one_day_sentiment_df.loc[i-1,'date'].weekday()==0:#previous row is sunday
                    monday_value1 = one_day_sentiment_df.loc[i-1,'two_day']*0.9
                    monday_checker1=1
                one_day_sentiment_df.loc[i,'two_day'] = (monday_value1+one_day_sentiment_df.loc[i,'two_day'])/(monday_checker1+1)
            else:
                one_day_sentiment_df.loc[i,'two_day'] = (one_day_sentiment_df.loc[i-1,'two_day']+one_day_sentiment_df.loc[i,'two_day'])/2
        elif i==2:###the same approach but when the thirs row then check sunday and saturday for monday and monday sunday for tuesday
            if one_day_sentiment_df.loc[i,'date'].weekday()==0:#if its monday
                sunday_value2=0#because only two record is above it
                sunday_checker2=0
                saturday_value2=0
                saturday_checker2=0
                if one_day_sentiment_df.loc[i-1,'date'].weekday()==6:#previous row is sunday
                    sunday_value2 = one_day_sentiment_df.loc[i-1,'two_day']*0.9
                    sunday_checker2=1
                if one_day_sentiment_df.loc[i-2,'date'].weekday()==5:#previous row is saturday
                    saturday_value2=one_day_sentiment_df.loc[i-2,'two_day']*0.8
                    saturday_checker2=1
                one_day_sentiment_df.loc[i,'two_day'] = (saturday_value2+sunday_value2+one_day_sentiment_df.loc[i,'two_day'])/(saturday_checker2+sunday_checker2+1)
            elif one_day_sentiment_df.loc[i,'date'].weekday()==1:#if its tuesday
                sunday_value4=0#because only two record is above it
                sunday_checker4=0
                monday_value4=0
                monday_checker4=0
                if one_day_sentiment_df.loc[i-1,'date'].weekday()==0:#previous row is monday
                    monday_value4 = one_day_sentiment_df.loc[i-1,'two_day']*0.9
                    monday_checker4=1
                if one_day_sentiment_df.loc[i-2,'date'].weekday()==6:#previous row is sunday
                    sunday_value4=one_day_sentiment_df.loc[i-2,'two_day']*0.8
                    sunday_checker4=1
                one_day_sentiment_df.loc[i,'two_day'] = (monday_value4+sunday_value4+one_day_sentiment_df.loc[i,'two_day'])/(monday_checker4+sunday_checker4+1)
            else:
                one_day_sentiment_df.loc[i,'two_day'] = (one_day_sentiment_df.loc[i-1,'two_day']+one_day_sentiment_df.loc[i,'two_day'])/2
        #End of weekend code
print(one_day_sentiment_df.head(30))

'''
    Three days
    In two_day we have already modified the code for weekends and so the weekends impact is already there
    Now for three days two approaches could be possible, we remove all the weekends data and then do the average
    or we keep all the weekends data and then do the average
    For three day sentiments the weekend data is not done anything because now the weekend data is dealt with
'''
one_day_sentiment_df['three_day'] = one_day_sentiment_df.apply(lambda row: row.avg_sentiment, axis=1)
for i in range(1,len(one_day_sentiment_df)):
    if i==0:
        one_day_sentiment_df.loc[i,'three_day'] = (0+one_day_sentiment_df.loc[i,'three_day'])
    elif i==1:
        one_day_sentiment_df.loc[i,'three_day'] = (one_day_sentiment_df.loc[i-1,'three_day']+one_day_sentiment_df.loc[i,'three_day'])/2
    else:
        one_day_sentiment_df.loc[i,'three_day'] = (one_day_sentiment_df.loc[i-2,'three_day']+one_day_sentiment_df.loc[i-1,'three_day']+one_day_sentiment_df.loc[i,'three_day'])/3

'''
    Need to drop the weekends data as those has no historical data
    And also remove new year
'''

for i in range(1,len(one_day_sentiment_df)):##Iterate through the complete dataframe
    day = one_day_sentiment_df.loc[i,'day']
    if (day==6 or day==7):###drop the rows data which is saturday and sunday
        one_day_sentiment_df = one_day_sentiment_df.drop(i)
        #print("dropping")
    #print(one_day_sentiment_df.loc[i,'date'].weekday())


####Plotting the data
#print(one_day_sentiment_df)
#one_day_sentiment_df = one_day_sentiment_df.head(900)
#one_day_sentiment_df=one_day_sentiment_df.tail(60)
print(one_day_sentiment_df.head(30))
#plt.plot(one_day_sentiment_df['date'],one_day_sentiment_df['avg_sentiment'])
plt.plot(one_day_sentiment_df['date'],one_day_sentiment_df['two_day'],'r')##Plot the graph for two_day
plt.plot(one_day_sentiment_df['date'],one_day_sentiment_df['three_day'],'g')##Plot the graph for three day
#plt.plot(one_day_sentiment_df['date'],one_day_sentiment_df['avg_pol1'])
#plt.plot(one_day_sentiment_df['date'],one_day_sentiment_df['avg_pol2'])
#plt.plot(one_day_sentiment_df['date'],one_day_sentiment_df['avg_pol3'])
#plt.plot(one_day_sentiment_df['date'],one_day_sentiment_df['avg_pol4'])
plt.xticks(rotation='vertical')
plt.show()

###1. How to deal with weekends
###2. Assigning priority to tweets by the most commonly arrived usernames (first:1.5, second: 1.4, third: 1.3, fourth: 1.2) [done]


###Saving into another excel sheet
workbook1 = xlsxwriter.Workbook('Twitter_dataset_obtained_from_twint/final_data_TELSTRA_with_sentiments_twoday_threeday.xlsx')
worksheet1 = workbook1.add_worksheet()
count=1
for index, each_day in one_day_sentiment_df.iterrows():
    cell1 = 'A'+str(count)
    cell2 = 'B'+str(count)
    cell3 = 'C'+str(count)
    cell4 = 'D'+str(count)
    worksheet1.write(str(cell1), str(each_day.date))##Col1 date
    worksheet1.write(str(cell2), each_day.avg_sentiment)##Col2 average sentiment
    worksheet1.write(str(cell3), each_day.two_day)##Col3 two day sentiment
    worksheet1.write(str(cell4), each_day.three_day)##Col4 three day sentiment
    count=count+1
workbook1.close()