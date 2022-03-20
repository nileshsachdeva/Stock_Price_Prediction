import { Box, Divider, Paper, Typography } from "@material-ui/core";
import { makeStyles } from "@material-ui/styles";
import { useMobileView } from "../../../common/utils";
import { Colors } from "../../../constants/colors";
import { StockStats } from "../../../dummyData/stats";
import { EarningBarChart } from "./BarChart";

const useStyles = makeStyles(({ breakpoints }) => ({
  container: {
    borderRadius: 10,
    padding: 25,
    flexGrow: 1,
    [breakpoints.down("sm")]: {
      padding: 20,
      paddingBottom: 0,
    },
    paddingBottom: 0,
  },
}));

export const RevenueEarning = ({ symbol }) => {
  const Stats = StockStats[symbol];
  const classes = useStyles();
  const isMobileView = useMobileView();

  return (
    <Paper className={classes.container} elevation={4} variant="outlined">
      <Box display="flex" justifyContent="space-between" alignItems="center">
        <Typography variant="h5">Revenue Earnings</Typography>
        <Box
          display="flex"
          gridGap={isMobileView ? 8 : 24}
          flexDirection={isMobileView ? "column" : "row"}
        >
          <Box display="flex" alignItems="center">
            <Box
              width={15}
              height={15}
              bgcolor={Colors.BLUE}
              borderRadius={50}
              mr={1}
            />
            <Typography variant="body2" style={{ opacity: 0.7 }}>
              Revenue
            </Typography>
          </Box>
          <Box display="flex" alignItems="center">
            <Box
              width={15}
              height={15}
              bgcolor={Colors.ORANGE}
              borderRadius={50}
              mr={1}
            />
            <Typography variant="body2" style={{ opacity: 0.7 }}>
              Earnings
            </Typography>
          </Box>
        </Box>
      </Box>
      <Divider style={{ marginTop: 15 }} />
      <Box
        display="flex"
        mt={2}
        mb={2}
        alignItems="center"
        justifyContent="space-between"
        height={280}
        gridGap={24}
      >
        <EarningBarChart
          data={Stats.company_earnings_last_2}
          title="Annual Revenue/Earnings"
        />
        <EarningBarChart
          data={Stats.company_quartely_earnings_last_2}
          title="Quaterly Revenue/Earnings (2021)"
        />
      </Box>
    </Paper>
  );
};
