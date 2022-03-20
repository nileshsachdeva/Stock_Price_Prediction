# Load libraries
import flask
from flask import request
from flask_cors import CORS, cross_origin
import numpy as np 
from keras.models import load_model
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import json
import requests as rq
from datetime import datetime as dtt, timedelta
import yfinance as yf
import sklearn_recommender as skr
from functools import reduce


# instantiate flask 
app = flask.Flask(__name__)
# MODEL_PATH = 'LSTM_Telstra_01-11-2020.h5'
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

MODEL_PATH = 'LSTM_Telstra_01-11-2020.h5'
modelnov1 = load_model(MODEL_PATH)

MODEL_PATH2 = 'LSTM_Telstra_16-11-2020.h5'
modelnov16 = load_model(MODEL_PATH2)
# model = load_model(MODEL_PATH)

MODEL_PATH3 = 'LSTM_Telstra_01-12-2020.h5'
modeldec1 = load_model(MODEL_PATH3)

MODEL_PATH4 = 'LSTM_Telstra_16-12-2020.h5'
modeldec16 = load_model(MODEL_PATH4)

MODEL_PATH5 = 'LSTM_Qantas_01-11-2020.h5'
Qmodelnov1 = load_model(MODEL_PATH5)

MODEL_PATH6 = 'LSTM_Qantas_16-11-2020.h5'
Qmodelnov16 = load_model(MODEL_PATH6)
# model = load_model(MODEL_PATH)

MODEL_PATH7 = 'LSTM_Qantas_01-12-2020.h5'
Qmodeldec1 = load_model(MODEL_PATH7)

MODEL_PATH8 = 'LSTM_Qantas_16-12-2020.h5'
Qmodeldec16 = load_model(MODEL_PATH8)


@app.route("/predict", methods=["GET"]) #?date=some-value
@cross_origin()
def predict():
    cpy = request.args.get('company')
    if(cpy == 'TLS'):
        url = 'https://uow-deepnet-dev.vercel.app/data/TLSYY.json'
    elif(cpy == 'QAN'):
        url = 'https://uow-deepnet-dev.vercel.app/data/QABSY.json'

    headers = {
    'Content-Type': 'application/json; charset=utf-8'
    }
    r = rq.get(url, headers=headers)
    files = r.json()

    r = json.dumps(files)
    lr = json.loads(r)
    dataset = pd.json_normalize(lr)

    dt = request.args.get('dt')
    d = dtt.strptime(dt, "%Y-%m-%d")

# Convert datetime object to date object.
    paramDate = d.date()
    
    nov1 = "2020-11-01"
    nov1 = dtt.strptime(nov1, "%Y-%m-%d").date()
    nov16 = "2020-11-16"
    nov16 = dtt.strptime(nov16, "%Y-%m-%d").date()
    dec1 = "2020-12-01"
    dec1 = dtt.strptime(dec1, "%Y-%m-%d").date()
    dec16 = "2020-12-16"
    dec16 = dtt.strptime(dec16, "%Y-%m-%d").date()
    # if request.method == 'POST':
    # date = request.args.get('date')
    # date = "2020-11-16"
    date = dt
    training_set = dataset
    training_set = dataset[dataset['Date']<date].copy()#Separate the dataset based on date
    companydataset = training_set
    testing_set = dataset[dataset['Date']>=date].copy()
   

    selected_columns = ['Open','High','Low','Close','Two_day_sentiment_tweets','AverageSentimentNews']#Mention the columns to be selected for the analysis purpose
    training_set = training_set[selected_columns]
    sc = MinMaxScaler()#setting the range between 0 and 1
    training_set_scaled = sc.fit_transform(training_set)
    X_train = []
    ###Setting the future days for which it needs to be predicted
    future_days = 5
    for i in range(90,training_set_scaled.shape[0]-future_days+1):
        if training_set_scaled.shape[1]==1:
            X_train.append(training_set_scaled[i-90:i, 0])#if only a single column is used then only append the first column
        else:
            X_train.append(training_set_scaled[i-90:i])#if multiple columns are used then append all columns
      

    X_train = np.array(X_train)

    scale1 = MinMaxScaler()
    scale1.min_,scale1.scale_ = sc.min_[0],sc.scale_[0]
  ###Sett   
    past_90_days = training_set.tail(90)##As the testing set must have access to the past 90 days of data and so the last 90 daya data is fetched from the training set
    testing_set = past_90_days.append(testing_set, ignore_index = True)
    testing_set = testing_set[selected_columns]
    print(testing_set.columns)

    testing_set = sc.transform(testing_set)##The testing set is also scaled using the minmax scaler

    X_test = []


    for i in range(90, testing_set.shape[0]-future_days+1):
        if training_set_scaled.shape[1]==1:
            X_test.append(testing_set[i-90:i, 0])
        else:
            X_test.append(testing_set[i-90:i])
            
    X_test = np.array(X_test)

    
    predictDate = np.array([X_test[0]])

                               
    if(paramDate < nov16):
        if(cpy == 'TLS'):
            predicted_stock_price = modelnov1.predict(predictDate)
        elif(cpy == 'QAN'):
            predicted_stock_price = Qmodelnov1.predict(predictDate)
    elif(paramDate < dec1 and paramDate > nov16):
        if(cpy == 'TLS'):
            predicted_stock_price = modelnov16.predict(predictDate)
        elif(cpy == 'QAN'):
            predicted_stock_price = Qmodelnov16.predict(predictDate)
    elif(paramDate < dec16 and paramDate > dec1 and paramDate > nov16):
        if(cpy == 'TLS'):
            predicted_stock_price = modeldec1.predict(predictDate)
        elif(cpy == 'QAN'):
            predicted_stock_price = Qmodeldec1.predict(predictDate)
    else:
        if(cpy == 'TLS'):
            predicted_stock_price = modeldec16.predict(predictDate)
        elif(cpy == 'QAN'):
            predicted_stock_price = Qmodeldec16.predict(predictDate)
        

    scale = MinMaxScaler()
    scale.min_,scale.scale_ = sc.min_[0],sc.scale_[0]
    predicted_stock_price = scale.inverse_transform(predicted_stock_price)
    
    lists = predicted_stock_price.tolist()

    ###Plot graphs with the whole duration, and show the comparison of actual vs prediction
    selected_columns_for_analysis = selected_columns
    if 'Date' not in selected_columns_for_analysis:
        selected_columns_for_analysis.append('Date')
    print(selected_columns_for_analysis)
    analysis_data = dataset[selected_columns_for_analysis]
    #print(analysis_data)
    # analysis_data = analysis_data[(analysis_data['Date'] > '2018-01-02') & (analysis_data['Date'] <= date)]
    analysis_data['Prediction'] = analysis_data['Open']
    print(analysis_data.tail())

    ##Append the prediction values to the dataframe
    training_set_length = len(analysis_data[analysis_data['Date']< date]) #'2020-11-01'])
    #print(predicted_stock_price)
    for i in range(0,len(predicted_stock_price[:,-1])):
    #print(training_set_length+i)
        analysis_data.loc[training_set_length+i,'Prediction'] = predicted_stock_price[i,0]
        #print(str(predicted_stock_price[i,:])+" "+str(predicted_stock_price[i,0]))
        if i==(len(predicted_stock_price[:,-1])-1):
            #print("Last one")
            for j in range(1,future_days):
                analysis_data.loc[training_set_length+i+j,'Prediction'] = predicted_stock_price[i,j]


    col = analysis_data.columns.get_loc("Prediction")
    analysis_data['sma_50'] = analysis_data.iloc[:,col].rolling(window=50).mean()##Just to check if the above command is implemented properly
    analysis_data['sma_200'] = analysis_data.iloc[:,col].rolling(window=200).mean()
     
    #creating an indexing column for ease of use
    analysis_data['ind'] = range(1, len(analysis_data) + 1)
    position = len(analysis_data[analysis_data['Date']< date])
    position = position + 5
    analysis_data = analysis_data[(analysis_data['ind'] > 1) & (analysis_data['ind'] <= position)] 
    analysis_data.drop('ind', axis=1, inplace=True)
    last_50_days = analysis_data.tail(50)
    highlight_dict_golden = {'index':[],'Open':[]}
    highlight_dict_death = {'index':[],'Open':[]}
    period = {'index':[],'Open':[]}


    analysis_data.fillna('', inplace=True)
    # data=analysis_data[['Date', 'Open', 'sma_50', 'sma_200']].to_numpy()
    data=analysis_data[['Date', 'Open', 'sma_50', 'sma_200']]
    data= data.to_json(orient='records', lines=True)
    
    ###Highlight the golden and death cross points
    for index, each_day in last_50_days.iterrows():
        period['index'].append(each_day['Date'])
        period['Open'].append(each_day['Open'])
        if each_day['sma_50']>each_day['sma_200']:
            highlight_dict_golden['index'].append(each_day['Date'])
            highlight_dict_golden['Open'].append(each_day['Open'])
        if each_day['sma_50']<each_day['sma_200']:
            highlight_dict_death['index'].append(each_day['Date'])
            highlight_dict_death['Open'].append(each_day['Open'])
    
    result = {"prediction":lists,"highlight_dict_death":highlight_dict_death ,"highlight_dict_golden":highlight_dict_golden, "data":data }
    
    return flask.jsonify(result)


def initialize_company(company_name):
    company = yf.Ticker(company_name)
    return company

def company_general_details(company):
    return company.info['logo_url'],company.info['sector'],company.info['industry'],company.info['longBusinessSummary']

def revenue_growth_func(company):
  company_earnings_last_2 = company.earnings.tail(2)
  company_earnings_last_2 = company_earnings_last_2.to_json(orient='index')
  company_quartely_earnings_last_2 = company.quarterly_earnings.tail(2)
  company_quartely_earnings_last_2 = company_quartely_earnings_last_2.to_json(orient='index')
  return company_earnings_last_2,company.info['revenueGrowth'],company.info['earningsGrowth'],company_quartely_earnings_last_2,company.info['revenueQuarterlyGrowth'],company.info['earningsQuarterlyGrowth']

def EPS(company):
    return company.info['trailingEps']

def roa(company):
    return company.info['returnOnAssets']

def roe(company):
    return company.info['returnOnEquity']

def pe_ratio(company):
    try:
        return company.info['trailingPE']
    except:
        return company.info['forwardPE']

def price_sales(company):
    return company.info['priceToSalesTrailing12Months']

def net_profit_margin(company):
    return company.info['profitMargins']

def gross_profit_margin(company):
    return company.info['grossMargins']

def operating_margin(company):
    return company.info['operatingMargins']

def price_to_book(company):
    return company.info['priceToBook'] 

def enterprise_multiple(company):
    return company.info['enterpriseValue'],company.info['ebitda'],company.info['enterpriseValue']/company.info['ebitda']  

def longTermDebt_to_TotalAssetss(company):
    annual_balance_sheet = company.balance_sheet
    annbalsheet = pd.DataFrame()
    annbalsheet['Long Term Debt'] = annual_balance_sheet.loc['Long Term Debt'][0:2]
    annbalsheet['Total Assets'] = annual_balance_sheet.loc['Total Assets'][0:2]
    annbalsheet['Date'] = (annual_balance_sheet.loc['Long Term Debt'][0:2].index).strftime("%d-%m-%Y")
    annbalsheet = (annbalsheet).to_json(orient='index')
    annual_longtermdebt_to_totalassets_ratio = annual_balance_sheet.loc['Long Term Debt'][0]/annual_balance_sheet.loc['Total Assets'][0]

    quartely_balance_sheet = company.quarterly_balance_sheet
    quarterbalsheet = pd.DataFrame()
    quarterbalsheet['Long Term Debt'] = quartely_balance_sheet.loc['Long Term Debt'][0:2]
    quarterbalsheet['Total Assets'] = quartely_balance_sheet.loc['Total Assets'][0:2]
    quarterbalsheet['Date'] = (quartely_balance_sheet.loc['Long Term Debt'][0:2].index).strftime("%d-%m-%Y")
    quarterbalsheet = (quarterbalsheet.reset_index()).to_json(orient='index')
    quarter_longtermdebt_to_totalassets_ratio = quartely_balance_sheet.loc['Long Term Debt'][0]/quartely_balance_sheet.loc['Total Assets'][0]
    return annbalsheet,annual_longtermdebt_to_totalassets_ratio,quarterbalsheet,quarter_longtermdebt_to_totalassets_ratio

def debt_to_equity(company):
    return company.info['debtToEquity']

def quick_ratio(company):   
    return company.info['quickRatio']

def dividend_details(company):
    return company.info['trailingAnnualDividendYield'],company.info['trailingAnnualDividendRate'],company.info['dividendRate'],company.info['dividendYield'],company.info['fiveYearAvgDividendYield']


def peg_ratio(company): 
    return company.info['pegRatio']

@app.route("/getstats", methods=["GET"]) #?date=some-value
@cross_origin()
def getstats():
    cpy = request.args.get('company')
    company = initialize_company(cpy + '.AX')
    # print(company.info.keys())
    company_data = {}

    company_data['logourl'], company_data['sector'], company_data['industry'], company_data['description'] = company_general_details(company)

    company_data['company_earnings_last_2'],company_data['revenueGrowth'],company_data['earningsGrowth'],company_data['company_quartely_earnings_last_2'],company_data['revenueQuarterlyGrowth'],company_data['earningsQuarterlyGrowth'] = revenue_growth_func(company)
    company_data['eps'] = EPS(company)
    company_data['roa'] = roa(company)
    company_data['roe'] = roe(company)
    company_data['price_earnings_ratio'] = pe_ratio(company)
    company_data['price_to_sales'] = price_sales(company)
    company_data['net_profit_margin'] = net_profit_margin(company)
    company_data['gross_profit_margin'] = gross_profit_margin(company)
    company_data['operating_margin'] = operating_margin(company)
    company_data['price_to_book_ratio'] = price_to_book(company)
    company_data['enterpriseValue'], company_data['EBITDA'], company_data['enterpriseMultiple'] = enterprise_multiple(company)
    company_data['debt_to_equity'] = debt_to_equity(company)
    company_data['quickRatio'] = quick_ratio(company)
    company_data['trailingAnnualDividendYield'],company_data['trailingAnnualDividendRate'],company_data['dividendRate'],company_data['dividendYield'],company_data['fiveYearAvgDividendYield'] = dividend_details(company)
    company_data['peg_ratio'] = peg_ratio(company)
    company_data['annbalsheet'],company_data['annual_longtermdebt_to_totalassets_ratio'],company_data['quarterbalsheet'],company_data['quarter_longtermdebt_to_totalassets_ratio'] = longTermDebt_to_TotalAssetss(company)

    return flask.jsonify(company_data)

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
    # print(stocks_data_similarity)##Companies with matching sector or industry will have higher similarity
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

@app.route("/similarity", methods=["GET"]) #?date=some-value
@cross_origin()
def similarity():
    url = 'https://uow-deepnet-dev.vercel.app/data/profile.json'

    headers = {
    'Content-Type': 'application/json; charset=utf-8'
    }
    r = rq.get(url, headers=headers)
    files = r.json()

    r = json.dumps(files)
    lr = json.loads(r)
    dataset = pd.DataFrame.from_dict(lr, orient='columns')
    profile = dataset[['symbol','sector','industry']]
    cpy = request.args.get('company')
    company = (cpy + '.AX')
    return flask.jsonify(similarity_stocks_sector_industry(profile,company,0.10))


def returns_and_volatility(wholedata):
  ###Fetch the historical records of all the 6 companies/stocks
  company1 = yf.Ticker("TLS.AX")
  company2 = yf.Ticker("QAN.AX")
  company3 = yf.Ticker("CWN.AX")
  company4 = yf.Ticker("FPH.AX")
  company5 = yf.Ticker("ANN.AX")
  company6 = yf.Ticker("TPG.AX")

  #Fetching recent data of companies of 1 year prior from today
  company1dataset = company1.history(period="1y")
  company1dataset.reset_index(inplace=True)
  company2dataset = company2.history(period="1y")
  company2dataset.reset_index(inplace=True)
  company3dataset = company3.history(period="1y")
  company3dataset.reset_index(inplace=True)
  company4dataset = company4.history(period="1y")
  company4dataset.reset_index(inplace=True)
  company5dataset = company5.history(period="1y")
  company5dataset.reset_index(inplace=True)
  company6dataset = company6.history(period="1y")
  company6dataset.reset_index(inplace=True)
  # print(company1dataset)
  
  all_comp_datasets = [company1dataset[['Date','Open']],company2dataset[['Date','Open']],company3dataset[['Date','Open']],company4dataset[['Date','Open']],company5dataset[['Date','Open']],company6dataset[['Date','Open']]]##get only the open and date for both dataset
  
  combined_data = reduce(lambda left,right: pd.merge(left,right,on='Date'), all_comp_datasets).iloc[:, 1:]##Next combines the dataset based on the date,
  
  #as all the stocks data are from same ASX and so same date will be there for all
  # print(combined_data.head())
  combined_data.columns = ["TLS.AX","QAN.AX","CWN.AX","FPH.AX","ANN.AX","TPG.AX"]
  if (wholedata == 'yearly'):
    ###Performing the analysis on the total data
    total_days = len(combined_data)
    stock_returns = combined_data.pct_change()##We compute the percentage change between each data which will record how fluctuating the data can get
    mean_stock_daily_returns_total = stock_returns.mean()
    stock_volatilities_total = stock_returns.std()
      
    analysis_result = pd.DataFrame({'returns': mean_stock_daily_returns_total * total_days,'volatility': stock_volatilities_total * total_days})
    print("yearly")
    return analysis_result
    # print(analysis_result)
  else:
  ###Performing the analysis on the last 60 day's data
    stock_returns_last_60_days = (combined_data.pct_change()).tail(60)##Get the last 60 days data of percetage change
    mean_stock_daily_returns_60days = stock_returns_last_60_days.mean()
    stock_volatilities_60days = stock_returns_last_60_days.std()
    analysis_result_60days = pd.DataFrame({'returns': mean_stock_daily_returns_60days * 60,'volatility': stock_volatilities_60days * 60})
    print("days")
    return analysis_result_60days
    # print(analysis_result_60days)


@app.route("/volatility", methods=["GET"]) #?date=some-value
@cross_origin()
def volatility():
    cpy = request.args.get('range')
    range = cpy
    return returns_and_volatility(range).to_json()


#Volume Recommendation
def volume_recommendation(companyname, startDate, EndDate):
    pd.options.mode.chained_assignment = None
    company = yf.Ticker(companyname)
    companydataset = company.history(start=startDate, end=EndDate) 
    companydataset.reset_index(inplace=True)
    QANdataset = companydataset[['Close','Volume']]
    # print(QANdataset)
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
    # print(QANdataset)
    
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
   
    #Scaling the sma values to be able to plot in a same graph
    sc = MinMaxScaler()#setting the range between 0 and 1
    QANdataset_scaled = sc.fit_transform(QANdataset)#Transform the training set into scaled features
    # print(QANdataset_scaled)
    close = []
    obv = []
    for sc in QANdataset_scaled:
        close.append(sc[3])
        obv.append(sc[4])

    result = QANdataset.to_json(orient="records")
    parsed = json.loads(result)
    json.dumps(parsed, indent=4)  
    close = json.dumps(close)
    obv = json.dumps(obv)
    results = json.dumps(results)
    result = {
        "unscaled": parsed,
        "scaled": {"close":close,"obv":obv,"result":results}
    }
# QANdataset, QANdataset_scaled
    return result

@app.route("/rvolume", methods=["GET"]) #?date=some-value
@cross_origin()
def rvolume():
    cpy = request.args.get('company')
    range = cpy + '.AX'
    sdt = request.args.get('sdt')
    edt = request.args.get('edt')
    v1 = volume_recommendation(range,sdt,edt)
    return v1


@app.route("/keepalive", methods=["GET"]) #?date=some-value
@cross_origin()
def keepalive():
    x =  "success"
    return flask.jsonify(x)


if __name__ == "__main__":
    app.run(host='127.0.0.2')
    # app.run(debug=True)