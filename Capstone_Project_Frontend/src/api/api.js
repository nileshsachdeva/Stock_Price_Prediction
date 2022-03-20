import axios from "axios";
import { STOCK_API_KEY } from "../constants/common";

// const ANALYSIS_API = 'https://stocks-uow.herokuapp.com/getstats?company=QAN'
const ANALYSIS_API = "https://stocks-uow.herokuapp.com";

export const fetchStockData = (symbol) =>
  axios.get(
    `https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=${symbol}&outputsize=full&apikey=${STOCK_API_KEY}`
  );

export const getNews = (queryText) =>
  axios.get(`https://uniproject-test.netlify.app/news?q=${queryText}`);

//2020-12-17&company=QAN
export const fetchRealtimePrediction = async (symbol, date) => {
  const res = await axios.get(
    `${ANALYSIS_API}/predict?dt=${date}&company=${symbol}`
  );
  return res.data;
};

export const fetchStockJson = async (symbol) => {
  const data = await axios.get(`/data/${symbol}.json`);
  return data.data;
};

export const fetchSimilarity = async (symbol) => {
  const res = await axios.get(`${ANALYSIS_API}/similarity?company=${symbol}`);
  return res.data;
};

export const fetchVolatility = async () => {
  const res = await axios.get(`${ANALYSIS_API}/volatility?range=yearly`);
  return res.data;
};

export const fetchVolumeReturnRecomm = async (symbol) => {
  const res = await axios.get(
    `${ANALYSIS_API}/rvolume?company=${symbol}&sdt=2020-01-02&edt=2020-12-28`
  );
  return res.data;
};
