import { Box, useMediaQuery } from "@material-ui/core";
import { DividendCard } from "./dividendCard";
import { InfoTableCard } from "./InfoTableCard";
import { StockStats } from "../../../dummyData/stats";

export const StatsCards = ({ symbol }) => {
  const stock = StockStats[symbol];
  const isMobile = useMediaQuery("(max-width:600px)");

  const infoTableData = [
    { name: "Earnings Growth", value: stock.earningsGrowth },
    { name: "Quarterly Earnings Growth", value: stock.earningsQuarterlyGrowth },
    { name: "Enterprise Value", value: stock.enterpriseValue },
    { name: "Enterprise Multiple", value: stock.enterpriseMultiple },
  ];

  return (
    <Box
      mt={4}
      mb={4}
      display="flex"
      flexDirection={isMobile ? "column" : "row"}
      gridGap={24}
    >
      <DividendCard
        rate={stock.dividendRate}
        yild={stock.dividendYield}
        avg={stock.fiveYearAvgDividendYield}
      />
      <InfoTableCard data={infoTableData} />
    </Box>
  );
};
