Project Name: Development of Stock Prediction and Recommendation System using Technical and Fundamental Analysis

Group Leader: Bikram Paul(6752767)
Team Members: Akhil Ramani (6750503)
			  Nilesh Sachdeva (6860114)
			  Pavithran Rajasekaran (6733268)
			  Rahul Bhadwal (6748934)

Project Supervisor: Prof. Lei Wang

Project Structure:
Mobile app APK
	stocks.apk
		Description/Purpose: This is an android apk installable file for android device which would install our stocks application for mobile device by which the user can view the webpage information and details about the stock prediction and recommendation system.
Experimental_study_analysis_result
	Stats_on_prediction_results.txt
	Stats_many_to_many.xlsx
	MSE_scores_of_models.xlsx
		Description/Purpose of this code: This is a not a code section but consists of excel/text files which consists of extra root-mean-squared error measurements that were computed by the group while experimenting with the hyper-parameters, important features and the number of future days prediction that the model could perform. These files are submitted for extra information purposes.
Code
	Recommendation Section Code
		Historical dataset for companies
			TPG.AX.csv
			TLS.AX.csv
			QAN.AX.csv
			FPH.AX.csv
			CWN.AX.csv
			ANN.AX.csv
				Description/Purpose: This folder consist of the historical records for the companies as csv files collected from 01/01/2018 to 01/01/2021.
		Recommendation_approaches_with_fixed_data.py
			Description/Purpose: This python file consists of the code for the four recommendation approaches and the data used for recommendation is collected from the historical fixed records and is not realtime.
		Recommendation_approaches_real_time_data.ipynb
			Description: This python file consists of the code for the four recommendation approaches and the data used for recommendation is collected on a realtime basis so that the data displayed on the frontend is the current data.
		Financial_Ratios_collector_for_Companies.ipynb
			Description/Purpose: This python file consists of the code for collection real-time information about the intrinsic value of the companies and fetch the financial ratios, earnings, assets, dividends data for the stock companies.
	Prediction Section Code
		Trained_models
			Description/Purpose: This folder consists of h5 files which are trained models to fasten the prediciton process, the model is trained for both companies using LSTM and GRU and for different number of future days 1,2,5 and 10.
		Final_datasets
			telstradataset.xlsx
			qantasdataset.xlsx
				Description/Purpose: This folder consists of the final datasets for both companies Telstra and Qantas. These dataset consists of all three historical records, tweets sentiment and news sentiment. The dataset consists of 14 features in total but only 6 features are being used in total for the model training and testing purpose.
		PredictionSystem_without_online_learning.ipynb
			Description/Purpose of this code: This code represents the prediction system where the dataset features are read, and then divided into training and test set, the data is formatted based on rnn structure, the model architecture is generated and then the model prediction results are compared with the actual data. The moving average is then computed for the company data which is also one of the recommendation approach.
		PredictionSystem_with_online_learning.ipynb
			Description/Purpose of this code: This code represents the prediciton system but with an additional component for online/incremental learning where the trained model is again fitted on new and unseen data with a low learning rate and the prediciton accuracy of the model is compared.
		Predictionsystem_ARIMA_and_Prophet.ipynb
			Description/Purpose of this code: This code consits of two models Arima and Prophet where it was tried to check if the model can predict the 'Open' price based on the data provided but these models had its limitations leading to the results being inaccurate and not precise.
	Data collection and preprocessing codes
		Tweets
			Samples of Tweets collected
				Telstra_twitter_tweets_dataset_2018-01.xlsx
				Telstra_sentiments_twoday_threeday_dataset.xlsx
				Telstra_combined_tweets_dataset_with_sentiments.xlsx
				Qantas_twitter_tweets_dataset_2018_01_03.xlsx
				Qantas_sentiments_twoday_threeday.xlsx
				Qantas_combined_tweets_dataset_with_sentiments.xlsx
					Description/Purpose: This folder consists of files which represents the tweets dataset that was used. The files consists of raw tweets that were collected based on keywords, the tweets pre-processed files, sentiment allocated, combined daywise and the final files for both the companies.
			1_Twitter_Tweets_Dataset_Collector_using_TWINT.py
			2_tweets_dataset_combiner.py
			3_tweets_daywise_sentiment_allocator.py
				Description/Purpose of these codes: These python files represent the codes to combine the tweets dataset collected manually, pre-process the dataset by performing the nlp operations, allocate sentiments and compute the average single day, two day and three day sentiments for the tweets dataset.
		News
			Samples of news headlines collected
				Telstra_news_data_Dec2017-Sep2018.xlsx
				Qantas_news_dataset_stage3.xlsx
				Qantas_news_dataset_stage2.xlsx
				Qantas_news_dataset_stage1.xlsx
				Qantas_news_dataset_stage0.xlsx
				Qantas_news_data_Dec2017-Sep2018.xlsx
					Description/Purpose: This folder consists of files which represents the news dataset that was used. The stage wise files are provided, representing the data that was gathered month wise, combined data, pre-processed data, data with sentiments and the final news data.
			1_news_dataset_combiner.py
			2_news_preprocessor_and_sentiment_allocator.py
			3_news_perday_sentiment_calculator.py
				Description/Purpose of these codes: These python files represent the codes to combine the news dataset collected manually, pre-process the dataset by performing the nlp operations, allocate sentiments and compute the average single day sentiments for the news dataset.
	mobileAppCode(dotnet)
		stocks-cap
			stocks-cap
			stocks-cap.sln
				Description/Purpose of this code: This code section is for the development of the mobile application for the system.
	RESTapi
		app.py
		LSTM_Qantas_01-11-2020.h5
		Procfile
		readme.txt
		requirements.txt
			Description/Purpose of this code: This code section represents an api that is used as a backend communicator that connects the front end and the prediciton+recommendation system. This code consists of requests that provides data to the front end by retrieving information from the prediciton+recommendation system.  
	Capstone_Project_Frontend
		Description/Purpose of this code: This folder consists of the code section for the front end system developed in React Js. The front end system receives data via the api requests and displays in an user-friendly way for the user to understand the prediciton and recommendation system results along with the important details of the intrinsic value of the company.