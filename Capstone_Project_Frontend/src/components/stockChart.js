import {
  makeStyles,
  Paper,
  Typography,
  Divider,
  LinearProgress,
  useMediaQuery,
  Box,
} from "@material-ui/core";
import moment from "moment";
import { useRef, useState } from "react";
import { useQuery } from "react-query";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  Tooltip,
  Rectangle,
  YAxis,
} from "recharts";
import { fetchStockJson } from "../api/api";

const useStyles = makeStyles((theme) => ({
  graphContainer: {
    height: 320,
    overflowX: "scroll",
    display: "flex",
    [theme.breakpoints.up("sm")]: {
      "&::-webkit-scrollbar": {
        display: "none",
      },
    },
  },
  graph: {
    fontFamily: theme.typography.fontFamily,
    "&>svg>g>g>g>text>tspan": {
      fontSize: 13,
      opacity: 0.6,
    },
  },
}));

export const StockChart = ({ symbol }) => {
  const classes = useStyles();
  const isMobile = useMediaQuery("(max-width:600px)");
  const graphEndRef = useRef(null);
  // const [stockChartData, setStockChartData] = useState()
  // const [loading, setLoading] = useState(true)

  const scrollToBottom = () => {
    setTimeout(
      () =>
        graphEndRef.current?.scrollIntoView({
          behavior: "smooth",
          block: "end",
          inline: "nearest",
        }),
      500
    );
  };

  const {
    data: stockChartData,
    isLoading,
    error,
  } = useQuery("stockData", () => fetchStockJson(symbol), {
    onSuccess: scrollToBottom,
  });

  // useEffect(() => {
  //   fetchStockData(symbol)
  //     .then(res => {
  //       const formattedData = Object.entries(res.data['Time Series (Daily)']).map(([date, dayRate]) => ({
  //         date,
  //         price: parseFloat(dayRate['1. open']),
  //         pred: parseFloat(dayRate['2. high'])
  //       }))
  //       setStockChartData(formattedData.reverse())
  //       setLoading(false)
  //     })
  //     .catch(e => console.log(e))
  // }, [])

  const _handleDateTick = (tick) => moment(tick, "YYYY-MM-DD").format("DD MMM");

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
        <Typography variant="caption">
          <b>{moment(label, "YYYY-MM-DD").format("DD MMM YYYY")}</b>
        </Typography>
        <Box display="flex" flexDirection="column">
          {payload.map((entry) => (
            <Typography variant="caption">
              {entry.name}: {entry.value?.toFixed(2)}
            </Typography>
          ))}
        </Box>
      </Box>
    );

  const CustomCursor = (props) => {
    const { points, height, stroke } = props;
    const [config, setConfig] = useState({ w: 1, c: stroke });
    const _handleCLick = () => {
      setConfig({ w: 1, c: "grey" });
      // setTimeout(()=>setConfig({w: 1, c: stroke}), 80)
    };
    return (
      <Rectangle
        fill={config.c}
        x={points[0].x}
        width={config.w}
        height={height}
        onMouseDownCapture={_handleCLick}
        onMouseUpCapture={() => setConfig({ w: 1, c: stroke })}
      />
    );
  };

  //#2b46a2
  return (
    <Paper
      style={{ padding: 25, borderRadius: 10, paddingBottom: 20 }}
      elevation={4}
      variant="outlined"
    >
      <Typography variant="h5">Forecasts</Typography>
      <Divider style={{ marginTop: 15 }} />
      <div className={classes.graphContainer} id="graph-container">
        {!isLoading ? (
          <ResponsiveContainer width={isMobile ? 700 : "100%"} height="100%">
            <LineChart
              data={stockChartData.slice(-100)}
              className={classes.graph}
            >
              <Line
                type="linear"
                dataKey="Open"
                stroke="#42435e"
                strokeWidth={2}
                dot={false}
              />
              <Line
                type="basis"
                dataKey="Prediction"
                stroke="rgb(255 12 0 / 45%)"
                dot={false}
                strokeWidth={10}
              />
              <XAxis
                padding={{ right: 30 }}
                dataKey="Date"
                tickFormatter={_handleDateTick}
              />
              <YAxis domain={["auto", "auto"]} hide />
              <Tooltip content={<CustomTooltip />} cursor={<CustomCursor />} />
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <LinearProgress color="secondary" style={{ opacity: 0.3 }} />
        )}
        <div ref={graphEndRef} />
      </div>
    </Paper>
  );
};
