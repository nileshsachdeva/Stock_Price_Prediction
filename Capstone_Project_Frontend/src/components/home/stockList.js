import { Box, Card, makeStyles } from "@material-ui/core";
import { StockListItem } from "./stockListItem";

const useStyles = makeStyles({
  scrollContainer: {
    "&::-webkit-scrollbar": {
      display: "none",
    },
    scrollbarWidth: "none",
  },
});

export const StockList = () => {
  const classes = useStyles();
  const stocks = [
    {
      name: "Telstra",
      logo: "telstra.png",
      symbol: "TLSYY",
      prediction: 0,
    },
    {
      name: "Qantas",
      logo: "qantas.png",
      symbol: "QABSY",
      prediction: 1,
    },
  ];

  return (
    <Box>
      <Box
        className={classes.scrollContainer}
        display="flex"
        gridGap={20}
        overflow="scroll"
        padding={1.5}
        margin={-1.5}
      >
        {stocks.map((stock, index) => (
          <StockListItem key={index} item={stock} />
        ))}
        <Card
          style={{
            width: 260,
            minWidth: 230,
            borderRadius: 15,
            backgroundColor: "#e8e8e8",
          }}
        />
        <Card
          style={{
            width: 260,
            minWidth: 230,
            borderRadius: 15,
            backgroundColor: "#e8e8e8",
          }}
        />
      </Box>
    </Box>
  );
};
