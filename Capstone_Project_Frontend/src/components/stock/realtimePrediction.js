import { useEffect, useState } from "react";
import {
  Box,
  Divider,
  LinearProgress,
  makeStyles,
  Paper,
  Typography,
  useMediaQuery,
} from "@material-ui/core";
import { Skeleton } from "@material-ui/lab";
import moment from "moment";
import {
  KeyboardDatePicker,
  MuiPickersUtilsProvider,
} from "@material-ui/pickers";
import DateFnsUtils from "@date-io/date-fns";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  Tooltip,
  YAxis,
} from "recharts";
import {
  formatRealtimePredictionData,
  getPredictionApiSymbol,
} from "../../common/utils";
import { fetchRealtimePrediction, fetchStockJson } from "../../api/api";
import { Colors } from "../../constants/colors";
import { useQuery } from "react-query";

const useStyles = makeStyles((theme) => ({
  graph: {
    // paddingLeft: 10,
    fontFamily: theme.typography.fontFamily,
    "&>svg>g>g>g>text>tspan": {
      fontSize: 13,
      opacity: 0.6,
    },
  },
}));

const CustomTooltip = ({ active, payload, label }) =>
  active && (
    <Box
      bgcolor="#fff"
      borderRadius={10}
      border="1px solid #dedede"
      boxShadow="0 2px 8px -1px #bababa"
      px={1.5}
      py={1}
    >
      {/* <Typography variant='caption' ><b>{moment(label).format('DD MMM YYYY')}</b></Typography> */}
      <Typography variant="caption">
        <b>{label}</b>
      </Typography>
      <Box display="flex" flexDirection="column">
        {/* {payload.map(entry => <Typography variant='caption' >{entry.name}: {entry.value.toFixed(2)}</Typography>)} */}
        {payload.map((entry) => (
          <Typography variant="caption">
            {entry.name}: {entry.value?.toFixed(3)}
          </Typography>
        ))}
      </Box>
    </Box>
  );

export const RealtimePrediction = ({ stockSymbol }) => {
  const classes = useStyles();
  const [date, setDate] = useState(new Date("Nov 02 2020"));
  const isMobileView = useMediaQuery("(max-width:600px)");
  const predictionSymbol = getPredictionApiSymbol(stockSymbol);
  const [predictionData, setPredictionData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [headerPred, setHeaderPred] = useState();

  const {
    data: stockData,
    isLoading: jsonLoading,
    error,
  } = useQuery("stockData", () => fetchStockJson(stockSymbol));

  useEffect(() => {
    setIsLoading(true);
    fetchRealtimePrediction(predictionSymbol, moment(date).format("YYYY-MM-DD"))
      .then((res) => setPredictionData(res.prediction))
      .catch((e) => console.log(e))
      .finally(() => setIsLoading(false));
  }, [date]);

  useEffect(() => {
    if (!jsonLoading) {
      const item = stockData.find(
        (data) => data.Date === moment(date).format("yyyy-MM-DD")
      );
      setHeaderPred(item?.Open?.toFixed(2));
    }
  }, [date, stockData]);

  function disableWeekends(date) {
    return date.getDay() === 0 || date.getDay() === 6;
  }

  return (
    <Box flexGrow={isMobileView ? "unset" : 1} display="flex">
      <Paper
        variant="outlined"
        style={{
          borderRadius: 10,
          padding: 20,
          paddingTop: 20,
          width: "100%",
          paddingBottom: 0,
        }}
      >
        <Box display="flex" justifyContent="space-between">
          <Typography variant="h5">Realtime Prediction</Typography>
          <Box display="flex" alignItems="center" gridGap={15}>
            <Box
              py={0.3}
              px={1}
              bgcolor={"rgb(49, 130, 189)"}
              color="#fff"
              borderRadius={10}
            >
              <Typography variant="body2" style={{ fontWeight: 700 }}>
                {headerPred}
              </Typography>
            </Box>
            <MuiPickersUtilsProvider utils={DateFnsUtils}>
              <KeyboardDatePicker
                format="dd MMM yyyy"
                value={date}
                color="secondary"
                variant={isMobileView ? "dialog" : "inline"}
                minDate={"Nov 01 2020"}
                maxDate={"Dec 23 2020"}
                onChange={setDate}
                style={{ width: 149 }}
                autoOk={true}
                disabled={isLoading}
                shouldDisableDate={disableWeekends}
              />
            </MuiPickersUtilsProvider>
          </Box>
        </Box>
        <Divider style={{ marginTop: 10 }} />
        {isLoading || !predictionData.length ? (
          <>
            <LinearProgress color="secondary" style={{ opacity: 0.3 }} />
            <Skeleton height={180} style={{ borderRadius: 10 }} />
          </>
        ) : (
          <Box mt={1} width="100%" height={188}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart
                data={formatRealtimePredictionData(predictionData[0], date)}
                className={classes.graph}
              >
                <Line
                  type="monotone"
                  dataKey="prediction"
                  strokeWidth={3}
                  dot={{ strokeWidth: 4 }}
                  animationDuration={500}
                />
                <XAxis
                  dataKey="date"
                  tickFormatter={(tick) => moment(tick).format("DD MMM")}
                  interval={"preserveStartEnd"}
                />
                <YAxis domain={["auto", "auto"]} hide />
                <Tooltip content={<CustomTooltip />} />
              </LineChart>
            </ResponsiveContainer>
          </Box>
        )}
      </Paper>
    </Box>
  );
};
