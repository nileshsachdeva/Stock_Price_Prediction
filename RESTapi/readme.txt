It is the REST API which uses pretrained model to predict the user given inputs. We have used the following endpoints in our React JS application. 

Flask webframework is hosted on free cloud service heroku with free tier plan. 

Prerequisite: Python installed with basic libraries. 

Instructions:
On Terminal, enter "python app.py" 


company can be QAN or TLS only. 

For running locally, replace https://stocks-uow.herokuapp.com/ with https://127.0.0.2:5000/ 
For local testing use date from 2020-11-03 to 2020-11-14 and company TLS only. Because of attached models limitation. 


1)  https://stocks-uow.herokuapp.com/predict?dt=2020-11-03&company=TLS
	Prediction for user input. Please use date from 2020-11-03 to 2020-12-23only. 

2)  https://stocks-uow.herokuapp.com/rvolume?company=QAN&sdt=2020-01-02&edt=2020-12-28
	Volume Return recommendation

3)  https://stocks-uow.herokuapp.com/similarity?company=QAN
	Similarity

4)  https://stocks-uow.herokuapp.com/volatility?range=yearly
	Volatility

5)  https://stocks-uow.herokuapp.com/getstats?company=TLS
	Company stats
