import {
  Box,
  Divider,
  Fade,
  Paper,
  Snackbar,
  Typography,
  useMediaQuery,
} from "@material-ui/core";
import { useState } from "react";
import { Button } from "../elements/button";

export const StockInfo = ({ stock, symbol }) => {
  const [snackOpen, setSanckOpen] = useState(false);

  const _handleBtnClick = () => {
    setSanckOpen(true);
    setTimeout(() => setSanckOpen(false), 2000);
  };

  const isMobileView = useMediaQuery("(max-width:600px)");

  return (
    <Box width={isMobileView ? "100%" : "55%"}>
      <Paper
        style={{
          borderRadius: 10,
          padding: isMobileView ? 20 : 25,
          paddingTop: 10,
        }}
        elevation={3}
        variant="outlined"
      >
        <Box display="flex">
          <Box>
            <Typography variant="body1" style={{ marginTop: 10, opacity: 0.5 }}>
              ASX:{symbol}
            </Typography>
            <Box display="flex" alignItems="center" mb={2} mt={2}>
              <img
                src={stock.logo}
                style={{ width: 30, marginRight: 10 }}
                alt={`${stock.name} logo`}
              />
              <Typography variant="h3">{stock.name}</Typography>
            </Box>
          </Box>
          <Box></Box>
        </Box>

        <Typography variant="body1" style={{ opacity: 0.7 }}>
          {stock.desc}
        </Typography>

        <Divider style={{ marginTop: 18 }} />
        <Box
          mt={2.6}
          gridGap={20}
          display="flex"
          flexDirection={isMobileView ? "column" : "row"}
        >
          <Button green onClick={_handleBtnClick}>
            Open position
          </Button>
          <Button red onClick={_handleBtnClick}>
            Close position
          </Button>
        </Box>
      </Paper>

      <Snackbar
        anchorOrigin={{ vertical: "top", horizontal: "center" }}
        message="Feature will be added in future!"
        open={snackOpen}
        TransitionComponent={Fade}
      />
    </Box>
  );
};
