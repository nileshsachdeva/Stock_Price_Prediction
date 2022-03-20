import {
  Paper,
  Box,
  Divider,
  Typography,
  Grid,
  useMediaQuery,
  makeStyles,
} from "@material-ui/core";
import { useEffect, useState } from "react";
import { getNews } from "../../../api/api";
import { NewsCard } from "./newsCard";

const useStyles = makeStyles(({ breakpoints }) => ({
  container: {
    borderRadius: 10,
    // marginTop: 24,
    padding: 25,
    [breakpoints.down("sm")]: {
      padding: 20,
      paddingBottom: 0,
    },
    paddingBottom: 0,
  },
}));

export const NewsContainer = ({ stockName }) => {
  const [newsList, setNewsList] = useState();
  const classes = useStyles();

  useEffect(() => {
    getNews(stockName)
      .then((res) => setNewsList(res.data.articles))
      .catch((e) => console.log(e));
  }, []);

  const isMobileView = useMediaQuery("(max-width:600px)");
  const bufferBox = !isMobileView && <Box height={3} />;
  return (
    <Paper className={classes.container} elevation={4} variant="outlined">
      <Typography variant="h5">Recent News</Typography>
      <Divider style={{ marginTop: 15 }} />
      <Box
        display="grid"
        gridTemplateColumns={isMobileView ? "auto" : "auto auto"}
        gridGap={5}
        height="70vh"
        overflow="scroll"
        style={{ overflowX: "hidden" }}
        mx={"-25px"}
      >
        {bufferBox}
        <Box height={3} />
        {newsList?.map((news) => (
          <NewsCard
            title={news.title}
            date={news.publishedAt}
            image={news.urlToImage}
            url={news.url}
          />
        ))}
        <Box height={3} />
        {bufferBox}
      </Box>
    </Paper>
  );
};
