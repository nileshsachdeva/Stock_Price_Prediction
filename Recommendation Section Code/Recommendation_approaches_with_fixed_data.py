import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

#pip install sklearn-recommender
from sklearn.feature_extraction.text import CountVectorizer
from scipy.spatial.distance import cosine
from sklearn.metrics.pairwise import cosine_similarity

import sklearn_recommender as skr
from functools import reduce
import seaborn as sns
import string
import re
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from datetime import datetime


##Generating the glove embeddings
def initialize_glove():
    #skr.glove.download('twitter')##Downloading the twitter glove embedding
    #skr.glove.download('wikipedia')##can also use wikipedia
    glove_transformed_data = skr.glove.GloVeTransformer('twitter', 50, 'sent', tokenizer=skr.nlp.tokenize_clean)##25 is the dimension
    #glove_transformed_data = skr.glove.GloVeTransformer('wikipedia', 300, 'sent', tokenizer=skr.nlp.tokenize_clean)##25 is the dimension
    ''' This consists of the word vector representations and the relation of the provided sentences with these glove vector'''
    return glove_transformed_data

##Method to create the stock profile with the symbol, sector, industry and description
def create_stock_profile():
    qantas_description = 'Qantas Airways Limited provides passenger and freight air transportation services in Australia and internationally. It operates through Qantas Domestic, Qantas International, Jetstar Group, and Qantas Loyalty segments. The company also offers air cargo and express freight services; and customer loyalty recognition programs. As of June 30, 2021, it operated a fleet of 311 aircraft under the Qantas and Jetstar brands. The company was founded in 1920 and is headquartered in Mascot, Australia.'
    
    telstra_description = 'Telstra Corporation Limited provides telecommunications and information services to businesses, governments, and individuals in Australia and internationally. It operates in four segments: Telstra Consumer and Small Business, Telstra Enterprise, Networks and IT, and Telstra InfraCo. The company offers telecommunication products, services, and solutions across mobiles, fixed and mobile broadband, telephony and Pay TV/IPTV, and digital content; and online self-service capabilities, as well as operates inbound and outbound call centers, owned and licensed Telstra shops, and the Telstra dealership network. It also provides sales and contract management; and product management services for data and Internet protocol networks, mobility services, and network applications and services products, such as managed network, unified communications, cloud, industry solutions, and integrated services and monitoring. In addition, the company engages in the development of industry vertical solutions; planning, design, engineering architecture, and construction of Telstra networks, technology, and information technology solutions; and delivering network technologies. Further, it provides telecommunication products and services through its networks and related support systems to other carriers, carriage service providers, and Internet service providers; access to fixed network infrastructure assets; disconnection services; and network services under the Infrastructure Services Agreement and commercial contracts, as well as holds fixed network infrastructure, including data centers, non-mobiles related domestic fiber, copper, HFC cable, international subsea cables, exchanges, poles, ducts, and pipes. The company was formerly known as Australian and Overseas Telecommunications Corporation Limited and changed its name to Telstra Corporation Limited in April 1993. Telstra Corporation Limited was founded in 1901 and is based in Melbourne, Australia.'

    crown_description = 'Crown Resorts Limited operates in the entertainment industry primarily in Australia. It operates through four segments: Crown Melbourne, Crown Perth, Crown Aspinalls, and Wagering & Online. The company owns and operates two integrated resorts, including Crown Melbourne and Crown Perth. Its Crown Melbourne resort comprises 2,628 gaming machines and 540 gaming tables; the Crown Towers Melbourne hotel with 481 guest rooms, the Crown Metropol Melbourne hotel with 658 guest rooms, and the Crown Promenade Melbourne hotel with 465 guest rooms; a conference center; banqueting facilities; restaurants and bars; and designer brands and retail outlets. The company\'s Crown Perth resort includes the Crown Towers Perth hotel with 500 guest rooms; the Crown Metropol Perth hotel comprising 397 guest rooms; the Crown Promenade Perth hotel with 291 guest rooms; 2,500 gaming machines and 350 gaming tables; a 1,500-seat Crown Ballroom and 2,300-seat Crown Theatre; convention facilities; and restaurants and bars, and a resort. It also owns and operates the Crown Aspinalls, a casino in London; and engages in wagering and online social gaming activities. The company was formerly known as Crown Limited and changed its name to Crown Resorts Limited in October 2013. Crown Resorts Limited was incorporated in 2007 and is based in Southbank, Australia.'

    fisher_description = 'Fisher & Paykel Healthcare Corporation Limited, together with its subsidiaries, designs, manufactures, markets, and sells medical device products and systems worldwide. It provides its products for use in acute and chronic respiratory care, and surgery, as well as the treatment of obstructive sleep apnea (OSA) in the home and hospital. The company offers Airvo 2, a humidified nasal high flow system; Optiflow, a nasal high flow therapy; and F&P 850 System, a noninvasive and invasive ventilation system. It also provides infant respiratory products, such as resuscitation, continuous positive airway pressure (CPAP) therapy, and nasal high flow therapy products. In addition, the company offers hospital products, including humidification products, breathing circuits, chambers, masks, nasal cannulas, surgical, accessories, and interfaces; and homecare products that include masks, CPAP devices, software and data management products, humidifiers, and accessories. Fisher & Paykel Healthcare Corporation Limited was founded in 1934 and is headquartered in Auckland, New Zealand.'

    ansell_description = 'Ansell Limited designs, develops, and manufactures protection solutions in the Asia Pacific, Europe, the Middle East, Africa, Latin America, the Caribbean, and North America. It operates in two segments, Healthcare and Industrial. The Healthcare segment manufactures and markets solutions comprising surgical gloves, single use and examination gloves, and clean and sterile gloves and garments, as well as consumables used by hospitals, surgical centers, dental practices, veterinary clinics, first responders, laboratories, and life sciences and pharmaceutical companies. The Industrial segment manufactures and markets hand and chemical protective clothing solutions for a range of industrial applications, including automotive, chemical, metal fabrication, machinery and equipment, food, construction, mining, oil and gas, and first responders. The company was formerly known as Pacific Dunlop Limited and changed its name to Ansell Limited in 2002. Ansell Limited was founded in 1893 and is based in Richmond, Australia.'
    
    tpg_description = 'TPG Telecom Limited provides telecommunications services. It owns and operates fixed and mobile network infrastructure, including fixed voice and data network with approximately 27,000 kilometers of metropolitan and inter-capital fiber networks; international subsea cable systems connecting Australia to principal hubs in North America and Asia; and mobile network. The company provides its fixed and mobile products under the Vodafone, TPG, iiNet, Internode, Lebara, and AAPT brands. The company, formerly known as Vodafone Hutchison Australia Limited, is based in North Sydney, Australia.'
    
    tcl_description = 'Transurban Group develops, operates, manages, and maintains toll road networks. It operates 21 toll roads in Sydney, Melbourne, and Brisbane in Australia; the Greater Washington area, the United States; and Montreal, Canada. The company is headquartered in Melbourne, Australia.'

    stocks_data  = {'symbol':['TLS','QAN','CWN','FPH','ANN','TPG','TCL'],'Company':['Telstra','Qantas','Crown Resorts Limited','Fisher & Paykel Healthcare Corporation Limited','Ansell Limited','TPG Telecom Limited','Transurban Group'],'sector':['Communication Services','Industrials','Consumer Cyclical','Healthcare','Healthcare','Communication Services','Industrials'],'industry':['Telecom Services','Airlines','Resorts & Casinos','Medical Instruments & Supplies','Medical Instruments & Supplies','Telecom Services','Infrastructure Operations'],'description':[telstra_description,qantas_description,crown_description,fisher_description,ansell_description,tpg_description,tcl_description]}#'exchange'}
    stocks_data = pd.DataFrame(stocks_data)
    return stocks_data

##Crates the n-dimensional embeddings for the stock description
def create_glove_embeddings_for_descriptions(glove_transformed_data,stocks_data):
    ##Forming the vector embeddings for both the descriptions
    embeddings = glove_transformed_data.transform(stocks_data['description'].fillna(""))###The description for the companies are converted into word vector glove embeddings
    stocks_data_embs = pd.concat([stocks_data['symbol'],pd.DataFrame(embeddings)],axis=1).set_index('symbol')
    ###This data consists of the symbol of the stock and the embeddings so 26d
    return stocks_data_embs


###Creates the similarity transformer data based on sector and industry and returns the stocks similar to a certain stock company
def similarity_stocks_sector_industry(stocks_data,symbol,sim_trans_threshold):
    #Performing one hot encoding for the data
    stocks_data_sector_dummy = pd.get_dummies(stocks_data['sector'], dummy_na=False, prefix='sector')###Set dummy_na = true if a column is required for NAN values
    #print(stocks_data_sector_dummy)
    
    stocks_data_industry_dummy = pd.get_dummies(stocks_data['industry'], dummy_na=False, prefix='industry')
    #print(stocks_data_industry_dummy)
    #df_exchange_dummy = pd.get_dummies(df_profile['exchange'], dummy_na=True, prefix='exchange')
    
    stocks_data_categories = pd.concat([stocks_data['symbol'], stocks_data_sector_dummy, stocks_data_industry_dummy], axis=1)
    #print(stocks_data_categories)##This dataframe will consist of the stock symbol and the one hot encoded of sector and industry

    # generating similarity matrix between the two company data
    sim_transformer = skr.transformer.SimilarityTransformer(cols=(1, None), index_col='symbol', normalize=True)
    stocks_data_similarity = sim_transformer.transform(stocks_data_categories)##The similarity matrix

    ##Printing the similarity matrix
    print(stocks_data_similarity)##Companies with matching sector or industry will have higher similarity
    '''This similarity is just a measure of the stocks that are related and nothing else'''
    
    ###Get the similarity matrix row for the company we are currently viewing
    df_row = stocks_data_similarity.loc[symbol].sort_values(ascending=False)##Getting the similarity value of the stock
    #print(symbol)
    df_row = df_row[df_row > sim_trans_threshold]##Getting the column with the simialrity value higher
    #print(df_row)
    similar_stocks = []
    for col in df_row.index:
        if isinstance(col, float): continue
        if col not in similar_stocks:
            if col!=symbol:
                similar_stocks.append(col)
    return symbol, similar_stocks
    

##Applyting knowledge based filtering as for a certain query the company descriptions will have those words or similar words
def knowledge_based_filtering_cosine_similarity(query,glove_transformed_data,stocks_data_embs,stocks_data,cos_similarity_threshold):
    ##Vector embedding the query
    query_embeddings = glove_transformed_data.transform([query])

    ##Then ranking each query based on the cosine similarity
    ranking_stocks_based_on_query = cosine_similarity(stocks_data_embs, query_embeddings)##Performing cosine similarity between the stock embeddings and the query
    
    ##The companies/stocks which are similar to certain companies might be of interest to the user
    stocks_data_result = pd.concat([stocks_data, pd.DataFrame(ranking_stocks_based_on_query, columns=['cosine'])], axis=1)

    print(stocks_data_result.sort_values(by='cosine', ascending=False).head())###This dataframe consists of the sector, industray and also the cosine similarity

    stocks_data_result = stocks_data_result[stocks_data_result['cosine'] > cos_similarity_threshold].dropna()
    ##Filtering out data which are above the cosine similarity
    
    return stocks_data_result

###Method to read each company data and compute their moving average of 50 and 200 days window
def moving_average_computation(symbol):
    folder_path = "Historical_dataset_for_companies\\"+symbol+".AX.csv"
    dataset = pd.read_csv(folder_path)##Read the company historical dataset
    #print(dataset.head())
    
    ###Simple moving average for 50 day window and 200 day window
    sma_50 = symbol+'SMA_50'
    sma_200 = symbol+ 'SMA_200'
    dataset[sma_50] = dataset.iloc[:,1].rolling(window=50).mean()##Just to check if the above command is implemented properly
    dataset[sma_200] = dataset.iloc[:,1].rolling(window=200).mean()
    #print(dataset.head(100))
    
    ###Exponential moving average with 50 day window as this performs better flow with the date, newer records is given more value
    ema_50 = symbol+'EMA_50'
    dataset[ema_50] = dataset.iloc[:,1].ewm(span=50,adjust=False).mean()
    
    ###Checking the golden and death cross in the data
    last_50_days = dataset.tail(50)
    #golden_cross_flag = 0
    #death_cross_flag = 0
    highlight_dict_golden = {'index':[],'Open':[],'Date':[]}
    highlight_dict_death = {'index':[],'Open':[],'Date':[]}
    period = {'index':[],'Open':[]}
    ###Highlight the golden and death cross points
    for index, each_day in last_50_days.iterrows():
        #print(each_day)
        period['index'].append(index)
        period['Open'].append(each_day['Open'])
        if each_day[sma_50]>each_day[sma_200]:
            highlight_dict_golden['index'].append(index)
            highlight_dict_golden['Open'].append(each_day['Open'])
            highlight_dict_golden['Date'].append(datetime.strptime(each_day['Date'],"%Y-%m-%d"))
        if each_day[sma_50]<each_day[sma_200]:
            highlight_dict_death['index'].append(index)
            highlight_dict_death['Open'].append(each_day['Open'])
            highlight_dict_death['Date'].append(datetime.strptime(each_day['Date'],"%Y-%m-%d"))
    #print(highlight_dict_golden)
    #print(highlight_dict_death)
    
    dataset['Date']=pd.to_datetime(dataset['Date'])
    ###All the plots for the data and golden and death crosses
    fig, ax = plt.subplots(figsize=(15,10))
    ax.grid(True)
    ax.plot(dataset['Date'],dataset['Open'],label='Stock Open Price')
    ax.plot(dataset['Date'],dataset[sma_50],label='SMA 50 days')
    ax.plot(dataset['Date'],dataset[sma_200],label='SMA 200 days')
    ax.plot(dataset['Date'],dataset[ema_50],label='EMA 50 days')
    ax.scatter(highlight_dict_golden['Date'],highlight_dict_golden['Open'],color="yellow",label="Golden period")
    ax.scatter(highlight_dict_death['Date'],highlight_dict_death['Open'],color="black",label="Death Period")
    ax.set_title("Golden/Death period analysis for stock:"+symbol,fontsize='xx-large')
    ax.set_xlabel('Date',fontsize='xx-large')
    ax.set_ylabel('Open Price',fontsize='xx-large')
    ax.xaxis_date()# interpret the x-axis values as dates
    fig.autofmt_xdate()# make space for and rotate the x-axis tick labels
    plt.xticks(fontsize='x-large')
    plt.yticks(fontsize='x-large')
    plt.legend(loc=2,fontsize="xx-large")
    plt.show()   
    return symbol,period,highlight_dict_golden,highlight_dict_death
    
##Method to compare the returns and volatilites of the companies/stocks
def returns_and_volatility():
    ###Read the datasets of all the 6 companies/stocks
    TLSdataset = pd.read_csv("Historical_dataset_for_companies\TLS.AX.csv")##Read the company historical dataset
    QANdataset = pd.read_csv("Historical_dataset_for_companies\QAN.AX.csv")##Read the company historical dataset
    CWNdataset = pd.read_csv("Historical_dataset_for_companies\CWN.AX.csv")##Read the company historical dataset
    FPHdataset = pd.read_csv("Historical_dataset_for_companies\FPH.AX.csv")##Read the company historical dataset
    ANNdataset = pd.read_csv("Historical_dataset_for_companies\ANN.AX.csv")##Read the company historical dataset
    TPGdataset = pd.read_csv("Historical_dataset_for_companies\TPG.AX.csv")##Read the company historical dataset
    
    all_comp_datasets = [TLSdataset[['Date','Open']],QANdataset[['Date','Open']],CWNdataset[['Date','Open']],FPHdataset[['Date','Open']],ANNdataset[['Date','Open']],TPGdataset[['Date','Open']]]##get only the open and date for both dataset
    
    combined_data = reduce(lambda left,right: pd.merge(left,right,on='Date'), all_comp_datasets).iloc[:, 1:]##Next combines the dataset based on the date,
    #as all the stocks data are from same ASX and so same date will be there for all
    print(combined_data.head())
    combined_data.columns = ['TLS','QAN','CWN','FPH','ANN','TPG']
    print(combined_data.corr())
    
    #print("Total days of historical data present = "+ str(len(combined_data)))##It consists of 761 rows of data
    
    ###Performing the analysis on the total data
    total_days = len(combined_data)
    stock_returns = combined_data.pct_change()##We compute the percentage change between each data which will record how fluctuating the data can get
    mean_stock_daily_returns_total = stock_returns.mean()
    #print(mean_stock_daily_returns_total)
    stock_volatilities_total = stock_returns.std()
    #print(stock_volatilities_total)
    
    analysis_result = pd.DataFrame({'returns': mean_stock_daily_returns_total * total_days,'volatility': stock_volatilities_total * total_days})
    #print(analysis_result)
    
    g = sns.jointplot(x="volatility",y="returns", data=analysis_result, kind="reg",height=7)

    plt.annotate('TLS', (analysis_result.iloc[0, 1], analysis_result.iloc[0, 0]))
    plt.annotate('QAN', (analysis_result.iloc[1, 1], analysis_result.iloc[1, 0]))
    plt.annotate('CWN', (analysis_result.iloc[2, 1], analysis_result.iloc[2, 0]))
    plt.annotate('FPH', (analysis_result.iloc[3, 1], analysis_result.iloc[3, 0]))
    plt.annotate('ANN', (analysis_result.iloc[4, 1], analysis_result.iloc[4, 0]))
    plt.annotate('TPG', (analysis_result.iloc[5, 1], analysis_result.iloc[5, 0]))
        
    plt.text(-10.0, -0.1, 'SELL', fontsize=10)
    plt.text(-10.5, 0.05, 'BUY', fontsize=10)
    plt.show()
    
    ###Performing the analysis on the last 60 day's data
    stock_returns_last_60_days = (combined_data.pct_change()).tail(60)##Get the last 60 days data of percetage change
    print(combined_data.tail(200).corr())
    mean_stock_daily_returns_60days = stock_returns_last_60_days.mean()
    stock_volatilities_60days = stock_returns_last_60_days.std()
    analysis_result_60days = pd.DataFrame({'returns': mean_stock_daily_returns_60days * 60,'volatility': stock_volatilities_60days * 60})
    print(analysis_result_60days)
    
    g = sns.jointplot(x="volatility",y="returns", data=analysis_result_60days, kind="reg",height=7)

    plt.annotate('TLS', (analysis_result_60days.iloc[0, 1], analysis_result_60days.iloc[0, 0]))
    plt.annotate('QAN', (analysis_result_60days.iloc[1, 1], analysis_result_60days.iloc[1, 0]))
    plt.annotate('CWN', (analysis_result_60days.iloc[2, 1], analysis_result_60days.iloc[2, 0]))
    plt.annotate('FPH', (analysis_result_60days.iloc[3, 1], analysis_result_60days.iloc[3, 0]))
    plt.annotate('ANN', (analysis_result_60days.iloc[4, 1], analysis_result_60days.iloc[4, 0]))
    plt.annotate('TPG', (analysis_result_60days.iloc[5, 1], analysis_result_60days.iloc[5, 0]))
    plt.text(1, -0.2, 'SELL', fontsize=10)
    plt.text(1, 0.2, 'BUY', fontsize=10)
    plt.show()
    
###Recommendation approaches using volume
#https://www.investopedia.com/articles/technical/02/010702.asp#:~:text=Volume%20measures%20the%20number%20of,gathering%20strength%20to%20the%20downside.
#https://www.investopedia.com/terms/o/onbalancevolume.asp
#https://school.stockcharts.com/doku.php?id=technical_indicators:on_balance_volume_obv
#https://randerson112358.medium.com/stock-trading-strategy-using-on-balance-volume-obv-python-77a7c719cdac

'''Final keypoints:
1) Price and OBV in sync like if both going up or down together then trend will continue
2) Price going down fast but obv is stable or going up then price will go up eventually again
3) Price going up fast but obv is going down then price will go down for sure
4) OBV is contnuously rising then the price will go up for sure
5) OBV is continuously falling then the price will go down for sure'''
def volume_recommendation():
    QANdataset = pd.read_csv("Historical_dataset_for_companies\QAN.AX.csv")
    QANdataset = QANdataset[['Date','Close','Volume']]
    print(QANdataset)
    QANdataset['OBV'] = 0
    ###calculate the obv values
    for i in range(0,len(QANdataset)):
        if i==0:
            QANdataset.loc[i,'OBV'] = QANdataset.loc[i,'Volume']
        else:##As per the conditions/formula the obv is calculated for the dataset
            if QANdataset.loc[i,'Close']==QANdataset.loc[i-1,'Close']:
                QANdataset.loc[i,'OBV'] = QANdataset.loc[i-1,'OBV']
            elif QANdataset.loc[i,'Close'] < QANdataset.loc[i-1,'Close']:
                QANdataset.loc[i,'OBV'] = QANdataset.loc[i-1,'OBV']-QANdataset.loc[i,'Volume']
            elif QANdataset.loc[i,'Close']>QANdataset.loc[i-1,'Close']:
                QANdataset.loc[i,'OBV'] = QANdataset.loc[i-1,'OBV']+QANdataset.loc[i,'Volume']
            else:
                QANdataset.loc[i,'OBV'] = QANdataset.loc[i-1,'OBV']
    QANdataset['Close_sma50'] = QANdataset['Close'].rolling(window=50).mean()##Calculate the simple moving average of the close
    QANdataset['OBV_sma50'] = QANdataset['OBV'].rolling(window=50).mean()##Calculate the simple moving average of the obv
    ##To generate the moving average of the movement to get the trend and the direction
    print(QANdataset)
    
    results = []
    ###As the first 50 values are null due to moving average and so those values are not considered
    for i in range(0,60):
        results.append(0)
    for i in range(60,len(QANdataset)):
        #compute the average of the last 10 days
        avg_close = 0
        avg_obv = 0
        for j in range(0,10):##Caluclating the average sma close and the average sma obv values to compare if the current value is moving upwards or downwards
            avg_close = avg_close + QANdataset.loc[i-j,'Close_sma50']
            avg_obv = avg_obv + QANdataset.loc[i-j,'OBV_sma50']
        avg_close = avg_close/10
        avg_obv = avg_obv/10
        ##Comparing the current sma values with the average values to determine if currently the trend is moving up or down
        if ((QANdataset.loc[i,'Close_sma50']>avg_close) and (QANdataset.loc[i,'OBV_sma50']>avg_obv)):
            results.append(1)
        elif ((QANdataset.loc[i,'Close_sma50']<avg_close) and (QANdataset.loc[i,'OBV_sma50']<avg_obv)):
            results.append(0)
        elif ((QANdataset.loc[i,'Close_sma50']<avg_close) and (QANdataset.loc[i,'OBV_sma50']>avg_obv)):
            results.append(1)
        elif ((QANdataset.loc[i,'Close_sma50']>avg_close) and (QANdataset.loc[i,'OBV_sma50']<avg_obv)):
            results.append(0)
        elif (QANdataset.loc[i,'OBV_sma50']>avg_obv):
            results.append(1)
        elif (QANdataset.loc[i,'OBV_sma50']<avg_obv):
            results.append(0)
    QANdataset['Date']=pd.to_datetime(QANdataset['Date'])
    fig,ax = plt.subplots(nrows=3,ncols=1,sharex=True,figsize=(10,8))
    ax[0].plot(QANdataset['Date'],QANdataset['OBV'],label="OBV")
    ax[0].plot(QANdataset['Date'],QANdataset['OBV_sma50'],label="OBV wth sma of 50")
    ax[1].plot(QANdataset['Date'],QANdataset['Close'],label="Close")
    ax[1].plot(QANdataset['Date'],QANdataset['Close_sma50'],label="Close with sma of 50")
    ax[2].plot(QANdataset['Date'],QANdataset['Volume'],label="Volume")
    ax[2].xaxis_date()# interpret the x-axis values as dates
    fig.autofmt_xdate()# make space for and rotate the x-axis tick labels
    ax[0].set_ylabel('OBV',fontsize='medium')
    ax[1].set_ylabel('Close',fontsize='medium')
    ax[2].set_xlabel('Date',fontsize='medium')
    ax[2].set_ylabel('Volume',fontsize='medium')
    ax[0].set_title('Onbalance Volume and Close price trend analysis (Qantas)',fontsize='medium')
    plt.xticks(fontsize='medium')
    plt.yticks(fontsize='medium')
    plt.legend(fontsize="medium")
    #ax.get_shared_x_axes().join(ax1, ax2, ax3)
    ax[0].legend()
    ax[1].legend()
    ax[2].legend()
    plt.show()
    #Scaling the sma values to be able to plot in a same graph
    sc = MinMaxScaler()#setting the range between 0 and 1
    QANdataset_scaled = sc.fit_transform(QANdataset[['Close','Volume','OBV','Close_sma50','OBV_sma50']])#Transform the training set into scaled features
    print(QANdataset_scaled)
    close = []
    obv = []
    #dates = []
    count=0
    for sc in QANdataset_scaled:
        close.append(sc[3])
        obv.append(sc[4])
        #dates.append(QANdataset.loc[count,'Date'])
        count=count+1
    #plt.figure()
    ###Plot 2 subplots
    #Subplot 1 is scaled sma close and scaled sma obv
    #Subplot 2 is the calculation of if the trend will continue to be up or low
    data = pd.DataFrame({'Scaled_Close':close,'Scaled_OBV':obv})
    data['Date']=QANdataset['Date']
    fig,ax = plt.subplots(nrows=2,ncols=1,sharex=False,figsize=(10,8))
    ax[0].plot(data['Date'],data['Scaled_Close'],label="Close scaled")
    ax[0].plot(data['Date'],data['Scaled_OBV'],label="OBV scaled")
    ax[1].plot(data['Date'],results,label="Close vs OBV")
    ax[0].set_ylabel('Scaled range',fontsize='medium')
    ax[0].set_xlabel('Date',fontsize='medium')
    ax[0].set_title('Comparison of Close and OBV trend (scaled data)',fontsize='medium')
    plt.xticks(fontsize='medium')
    plt.yticks(fontsize='medium')
    plt.legend(fontsize="medium")
    ax[0].xaxis_date()# interpret the x-axis values as dates
    fig.autofmt_xdate()# make space for and rotate the x-axis tick labels
    ax[0].legend()
    ax[1].legend()
    plt.show()
    
    

##The main function to perform recommendation and return results
if __name__ == "__main__":
    ###Step 1 should be to get related companies based on similarity transformer
        ###For example: People dealing with healthcare stocks then show other companies which are also dealing with healthcare sector
    #glove_transformed_data = initialize_glove()
    
    
    stocks_data = create_stock_profile()##Returns the dataframe with the stock data/profile
    print(stocks_data)##This dataframe consists of the company/stock details
    
    '''###Recommendation section 1: based on sector and industry
    sim_trans_threshold = 0.10###This is a threshold to get companies which are from the same sector and industry
    symbol = 'QAN'##The company im currently looking the data at
    symbol, similar_stocks = similarity_stocks_sector_industry(stocks_data,symbol,sim_trans_threshold)##Generates the similarity transformer matrix and then returns the stocks similar to a certain stock
    print("Currently viewing stocks of :" + str(symbol) + " and the other related companies would be " + str(similar_stocks))
    
    ###The previous print statement will give companies which match the company sector and industry'''
    
    '''###Recommendation section 2: based on keyword
    ###Next section will cover recommendations based on a certain keyword, such as people looking for stocks in communication, resorts and so on
    stocks_data_embs = create_glove_embeddings_for_descriptions(glove_transformed_data,stocks_data)##Returns the embedded dataframe
    print(stocks_data_embs)
    
    keyword = 'hospitality service flight'###Looking for stocks which match a certain query or company or sector
    cos_similarity_threshold = 0.75###This is a threshold to get companies which match the query keyword
    stocks_data_result = knowledge_based_filtering_cosine_similarity(keyword,glove_transformed_data,stocks_data_embs,stocks_data,cos_similarity_threshold)
    
    print(stocks_data_result)
    print("Stocks that are relevant to the keyword")
    for index, each_revelant_stock in stocks_data_result.iterrows():
        print(each_revelant_stock)'''
    
    
    ###Recommendation section 3: based on moving average trend
    '''stock_companies_symbols = ['TLS','QAN','CWN','FPH','ANN','TPG']
    company_data_after_analysis = {'symbol':[],'last_50_days':[],'golden_period':[],'death_period':[]}
    for symbol in stock_companies_symbols:
        ##Performs the moving average and returns data like the last 50 days, golden preiods and death crosses of companies
        symbol,last_50_days,highlight_dict_golden,highlight_dict_death = moving_average_computation(symbol)
        company_data_after_analysis['symbol'].append(symbol)
        company_data_after_analysis['last_50_days'].append(last_50_days)
        company_data_after_analysis['golden_period'].append(highlight_dict_golden)
        company_data_after_analysis['death_period'].append(highlight_dict_death)
    print(company_data_after_analysis)
    
    ###Plot of comparison of all companies and their trends
    plt.figure(figsize=[15,10])
    plt.grid(True)
    
    for i in range(0,len(company_data_after_analysis['symbol'])):
        print(company_data_after_analysis['symbol'][i])
        plt.plot(company_data_after_analysis['last_50_days'][i]['index'],company_data_after_analysis['last_50_days'][i]['Open'],label=company_data_after_analysis['symbol'][i]+'data')
        plt.scatter(company_data_after_analysis['golden_period'][i]['index'],company_data_after_analysis['golden_period'][i]['Open'],color="yellow")
        plt.scatter(company_data_after_analysis['death_period'][i]['index'],company_data_after_analysis['death_period'][i]['Open'],color="black")
    plt.xlabel('Days')
    plt.ylabel('Open')
    plt.legend(loc=2)
    plt.title('Company stock comparisons')
    plt.show()'''
    
    ###Recommendation section 4: the returns and the volatalities of the company datas will be checked and compared
    #returns_and_volatility()
    ###Recommendation section 5: the obv and the close trends are used to check the future direction of the stock trend
    volume_recommendation()
    
    print("Thats all 4 recommendation approaches")