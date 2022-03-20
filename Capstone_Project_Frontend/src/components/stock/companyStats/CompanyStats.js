import { Box, Divider, Paper, Typography } from "@material-ui/core";
import { makeStyles } from "@material-ui/styles";
import { EarningBarChart } from "./BarChart";
import { StockStats } from "../../../dummyData/stats";
import { BalanceSheet } from "./BalanceSheet";
import { Colors } from "../../../constants/colors";
import { Ratios } from "./Ratios";

const useStyles = makeStyles(({ breakpoints }) => ({
  container: {
    borderRadius: 10,
    marginTop: 24,
    marginBottom: 24,
    padding: 25,
    [breakpoints.down("sm")]: {
      padding: 20,
      paddingBottom: 0,
    },
    paddingBottom: 0,
  },
}));

export const CompanyStats = ({ symbol }) => {
  const Stats = StockStats[symbol];
  const RatioData = [
    {
      fill: Colors.BLUE,
      name: "Annual Long-Term Debt to Assets",
      value: Stats.annual_longtermdebt_to_totalassets_ratio,
    },
    {
      fill: Colors.RED_1,
      name: "Quarter Long-Term Debt to Assets",
      value: Stats.quarter_longtermdebt_to_totalassets_ratio,
    },
    {
      fill: Colors.ORANGE,
      name: "Debt-to-Equity",
      value: Stats.debt_to_equity,
    },
    {
      fill: Colors.GREEN_1,
      name: "Price/Earnings-to-Growth",
      value: Stats.peg_ratio,
    },
    {
      fill: Colors.YELLOW,
      name: "Price-to-Earnings",
      value: Stats.price_earnings_ratio,
    },
    {
      fill: Colors.DARK_BLUE,
      name: "Price-to-Book",
      value: Stats.price_to_book_ratio,
    },
    {
      fill: Colors.GREEN_2,
      name: "Price-to-Sales",
      value: Stats.price_to_sales,
    },
    { fill: Colors.RADIUM, name: "Quick Ratio", value: Stats.quickRatio },
  ];

  const classes = useStyles();

  return (
    <Paper className={classes.container} elevation={4} variant="outlined">
      <Box display="flex" alignItems="center" justifyContent="space-between">
        <Typography variant="h5">Balance Sheet</Typography>
        <Box display="flex" alignItems="center" gridGap={30}>
          <Box display="flex" alignItems="center">
            <Box
              width={15}
              height={15}
              borderRadius={50}
              bgcolor={Colors.BLUE}
              mr={1}
            />
            <Typography variant="body2">Assets</Typography>
          </Box>
          <Box display="flex" alignItems="center">
            <Box
              width={15}
              height={15}
              borderRadius={50}
              bgcolor={Colors.ORANGE}
              mr={1}
            />
            <Typography variant="body2">Debt</Typography>
          </Box>
        </Box>
      </Box>
      <Divider style={{ marginTop: 15 }} />
      <Box py={2}>
        <BalanceSheet
          annualData={Stats.annbalsheet}
          quarterData={Stats.quarterbalsheet}
        />

        <Divider style={{ marginTop: 24 }} />

        <Ratios data={RatioData} />
      </Box>
    </Paper>
  );
};
