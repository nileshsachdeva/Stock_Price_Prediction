import {
  Box,
  Paper,
  Typography,
  Divider,
  useMediaQuery,
  LinearProgress,
} from "@material-ui/core";
import { useQuery } from "react-query";
import { fetchVolatility } from "../../../api/api";
import { ReturnsRecommandation } from "./ReturnsRecommandation";
import { VoletalityRecommandation } from "./VoletalityRecommandation";

export const Recommandation = () => {
  const isMobile = useMediaQuery("(max-width:600px)");
  const { data, isLoading } = useQuery("voletality", () => fetchVolatility());

  return (
    <Paper
      style={{
        padding: 25,
        borderRadius: 10,
        paddingBottom: 0,
        marginTop: 24,
        marginBottom: 20,
      }}
      elevation={4}
      variant="outlined"
    >
      <Typography variant="h5">Recommendations</Typography>
      <Divider style={{ marginTop: 15 }} />
      {isLoading ? (
        <Box height={460}>
          <LinearProgress style={{ opacity: 0.6 }} />
        </Box>
      ) : (
        <Box
          py={4}
          display="flex"
          alignItems="center"
          justifyContent="space-around"
          flexDirection={isMobile ? "column" : "row"}
        >
          <Box
            display="flex"
            width="100%"
            flexDirection="column"
            alignItems="center"
          >
            <VoletalityRecommandation
              data={data.volatility}
              isMobile={isMobile}
            />
            <Typography variant="body2" style={{ opacity: 0.6 }}>
              <b>Volatility</b>
            </Typography>
          </Box>
          {isMobile && <Divider style={{ margin: "40px 0", width: "100%" }} />}
          <Box
            display="flex"
            flexDirection="column"
            alignItems="center"
            height="100%"
            width="100%"
          >
            <ReturnsRecommandation data={data.returns} isMobile={isMobile} />
            <Typography variant="body2" style={{ opacity: 0.6 }}>
              <b>Returns</b>
            </Typography>
          </Box>
        </Box>
      )}
      <Box my={3}>
        <Typography variant="h6">Description</Typography>
        <Divider style={{ marginTop: 15 }} />
        <Box style={{ opacity: 0.7 }}>
          <Typography
            variant="body1"
            style={{ marginTop: 25, marginBottom: 10 }}
          >
            <b>Volatility</b>
          </Typography>
          <Typography variant="body2">
            Volatility is an indication of stock price fluctuation over time. 
            The volatility score is computed by the standard deviation of 
            logarithmic returns. High volatility score indicates that the 
            stock price is not stable and could rise or fall often and low 
            volatility score indicates that the stock price is stable.
          </Typography>
          <Typography
            variant="body1"
            style={{ marginTop: 25, marginBottom: 10 }}
          >
            <b>Return</b>
          </Typography>
          <Typography variant="body2">
             Return is any change in the value of investment and is computed by 
             the average/mean percentage change of the “Open” price. In general, 
             the positive value of return indicates that the stock price is 
             expected to rise, and the negative value indicates that the stock 
             price is expected to fall.
          </Typography>
        </Box>
      </Box>
    </Paper>
  );
};
