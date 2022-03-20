import {
  Box,
  Divider,
  makeStyles,
  Paper,
  Typography,
  useTheme,
} from "@material-ui/core";

const useStyles = makeStyles({
  conatiner: {
    display: "flex",
    flexGrow: 1,
    borderRadius: 20,
    overflow: "hidden",
  },
});

const Row = ({ name, value }) => (
  <Box
    py={1.5}
    px={5}
    display="flex"
    alignItems="center"
    justifyContent="space-between"
    sx={{ "&:hover": { backgroundColor: useTheme().palette.action.hover } }}
    flexGrow={1}
  >
    <Typography
      variant="body1"
      style={{ fontSize: 15, fontWeight: 500, opacity: 0.6 }}
    >
      {name}
    </Typography>
    <Typography
      style={{ fontWeight: 700, opacity: 0.5, letterSpacing: 2 }}
      variant="body1"
    >
      {value}
    </Typography>
  </Box>
);

export const InfoTableCard = ({ data }) => {
  const classes = useStyles();

  return (
    <Paper className={classes.conatiner}>
      <Box display="flex" flexDirection="column" width="100%">
        {data.map((itm) => (
          <>
            <Row name={itm.name} value={itm.value?.toFixed(3)} />
            <Divider />
          </>
        ))}
        {/* <Row /> */}
        {/* <Divider />
        <Row /> */}
      </Box>
    </Paper>
  );
};
