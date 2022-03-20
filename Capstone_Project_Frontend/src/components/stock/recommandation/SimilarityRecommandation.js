import { Box, Paper, Typography } from "@material-ui/core";
import { Skeleton } from "@material-ui/lab";
import { useQuery } from "react-query";
import { fetchSimilarity } from "../../../api/api";
import { getPredictionApiSymbol, useMobileView } from "../../../common/utils";

export const SimilarityRecommandation = ({ symbol }) => {
  const { data, isLoading } = useQuery("similarity", () =>
    fetchSimilarity(getPredictionApiSymbol(symbol))
  );
  return (
    <Paper
      variant="outlined"
      style={{
        borderRadius: 10,
        padding: 20,
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
      }}
    >
      <Typography variant="h5">Similarity Analysis</Typography>
      <Box display="flex" alignItems="center" gridGap={10}>
        {isLoading ? (
          <Skeleton width={200} height={60} style={{ margin: "-20px 0" }} />
        ) : (
          <>
            <img
              src={`/assets/${data[1][0]}.png`}
              alt="company icon"
              height={25}
            />
            <Typography
              variant={"h4"}
              style={{ opacity: 0.7, marginBottom: -4 }}
            >
              {data[1][0]}
            </Typography>
          </>
        )}
      </Box>
    </Paper>
  );
};
