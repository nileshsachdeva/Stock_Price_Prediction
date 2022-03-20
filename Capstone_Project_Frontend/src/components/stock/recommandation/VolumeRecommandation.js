import {
  Box,
  Divider,
  LinearProgress,
  Paper,
  Typography,
  useMediaQuery,
} from "@material-ui/core";
import { makeStyles } from "@material-ui/styles";
import clsx from "clsx";
import { useQuery } from "react-query";
import {
  Bar,
  BarChart,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  YAxis,
} from "recharts";
import { fetchVolumeReturnRecomm } from "../../../api/api";
import { getPredictionApiSymbol } from "../../../common/utils";
import { Colors } from "../../../constants/colors";
import { VolumeData } from "../../../dummyData/volumeData";

const useStyles = makeStyles({
  container: {
    display: "flex",
    flexDirection: "column",
    padding: 25,
    borderRadius: 10,
    paddingBottom: 0,
    marginTop: 24,
    marginBottom: 24,
  },
  verticalText: {
    fontSize: 12,
    opacity: 0.6,
    textOverflow: "ellipsis",
    whiteSpace: "nowrap",
  },
  transform: {
    transform: "rotate(-90deg) translate(-110px)",
  },
});

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
      <Box display="flex" flexDirection="column">
        {/* {payload.map(entry => <Typography variant='caption' >{entry.name}: {entry.value.toFixed(2)}</Typography>)} */}
        {payload.map((entry) => (
          <Typography variant="caption">
            <b style={{ color: entry.stroke }}>{entry.name}</b>:{" "}
            {entry.value?.toFixed(3)}
          </Typography>
        ))}
      </Box>
    </Box>
  );

export const VolumeRecommandation = ({ symbol }) => {
  const classes = useStyles();
  const isMobile = useMediaQuery("(max-width:600px)");

  const { data, isLoading } = useQuery("volumeChart", () =>
    fetchVolumeReturnRecomm(getPredictionApiSymbol(symbol))
  );

  return (
    <Paper className={classes.container} variant="outlined">
      <Typography variant="h5">Volume Return Recommendation</Typography>
      <Divider style={{ marginTop: 15 }} />
      {/* {isLoading || !data ? ( */}
      {isLoading || !data ? (
        <>
          <LinearProgress style={{ opacity: 0.5 }} />
          <Box
            p={2}
            height={400}
            display="flex"
            alignItems="center"
            justifyContent="center"
          >
            {!data && !isLoading && (
              <Typography variant="h6" style={{ opacity: 0.3 }}>
                Error in data fetching
              </Typography>
            )}
          </Box>
        </>
      ) : (
        <Box p={0}>
          <Box width="100%" overflow="auto">
            <Box position="absolute" left={isMobile && 30}>
              <Box width={15} height={200} flexShrink={0}>
                <Typography
                  className={clsx(classes.verticalText, classes.transform)}
                >
                  Close-Price
                </Typography>
              </Box>
              <Box width={15} height={200} flexShrink={0}>
                <Typography
                  className={clsx(classes.verticalText, classes.transform)}
                >
                  OBV
                </Typography>
              </Box>
              <Box width={15} height={100} flexShrink={0}>
                <Typography
                  className={classes.verticalText}
                  style={{
                    transform: "rotate(-90deg) translate(-50px)",
                  }}
                >
                  Volume
                </Typography>
              </Box>
            </Box>

            <Box width={isMobile ? 1000 : "100%"}>
              <Box width="100%" height={200}>
                <ResponsiveContainer width={"100%"} height="100%">
                  <LineChart data={data.unscaled}>
                    {/* <LineChart data={VolumeData.unscaled}> */}
                    <Line
                      type="monotone"
                      dataKey="Close"
                      stroke={Colors.GREEN_2}
                      strokeWidth={2}
                      dot={false}
                    />
                    <Line
                      type="monotone"
                      dataKey="Close_sma50"
                      strokeWidth={2}
                      dot={false}
                    />
                    <Tooltip content={<CustomTooltip />} />
                    <YAxis domain={["dataMin", "dataMax"]} hide />
                  </LineChart>
                </ResponsiveContainer>
              </Box>
              <Box width={"100%"} height={200}>
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={VolumeData.unscaled}>
                    <Line
                      type="monotone"
                      dataKey="OBV"
                      strokeWidth={2}
                      dot={false}
                      stroke={Colors.ORANGE}
                    />
                    <Line
                      type="monotone"
                      dataKey="OBV_sma50"
                      strokeWidth={2}
                      dot={false}
                      stroke={Colors.YELLOW}
                    />
                    <Tooltip content={<CustomTooltip />} />
                    <YAxis domain={["dataMin", "dataMax"]} hide />
                  </LineChart>
                </ResponsiveContainer>
              </Box>
              <Box width={"100%"} height={100} mb={0}>
                <ResponsiveContainer height="100%" width="100%">
                  <BarChart data={VolumeData.unscaled}>
                    <Tooltip content={<CustomTooltip />} />
                    <Bar dataKey="Volume" fill="#4a4a4a" />
                  </BarChart>
                </ResponsiveContainer>
              </Box>
            </Box>
          </Box>
        </Box>
      )}
    </Paper>
  );
};
