import { Paper, Typography, Box, useMediaQuery } from "@material-ui/core";
import { makeStyles } from "@material-ui/styles";

const useStyle = makeStyles((theme) => ({
  container: {
    borderRadius: 50,
    maxWidth: 200,
    display: "flex",
    [theme.breakpoints.down("md")]: {
      borderRadius: 30,
    },
  },
  nameTxt: {
    fontSize: 17,
    fontWeight: 600,
    opacity: 0.45,
    textTransform: "uppercase",
    letterSpacing: 1.3,
    textAlign: "center",
    marginBottom: -5,
    marginTop: 5,
    [theme.breakpoints.down("md")]: {
      fontSize: 12,
      marginTop: 0,
    },
  },
}));

const InfoCard = ({ name, value, smallFont }) => {
  const classes = useStyle();
  const isMobile = useMediaQuery("(max-width:600px)");
  return (
    <Paper className={classes.container}>
      <Box
        p={isMobile ? 2 : 4}
        display="flex"
        flexDirection="column"
        alignItems="center"
        justifyContent="space-between"
      >
        <Typography
          variant="h3"
          style={{
            marginBottom: 10,
            fontSize: isMobile ? (smallFont ? 20 : 30) : smallFont ? 36 : 45,
            opacity: 0.5,
          }}
        >
          {value ? (
            <>
              {value}
              <text style={{ fontSize: isMobile ? 15 : 25 }}>%</text>
            </>
          ) : (
            "-"
          )}
        </Typography>
        <Typography className={classes.nameTxt} variant="body1">
          {name}
        </Typography>
      </Box>
    </Paper>
  );
};

export const DividendCard = ({ rate, yild, avg }) => {
  const isMobile = useMediaQuery("(max-width:600px)");

  return (
    <Box display="flex" gridGap={isMobile ? 18 : 24}>
      <InfoCard name="Dividend Rate" value={rate} />
      <InfoCard
        name="Dividend Yield"
        value={yild}
        smallFont={yild && toString(yild).length > 3}
      />
      <InfoCard name="Dividend Yield 5y avg." value={avg} />
    </Box>
  );
};
