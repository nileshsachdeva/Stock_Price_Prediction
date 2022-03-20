import {
  Box,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from "@material-ui/core";
import { withStyles } from "@material-ui/styles";
import {
  Bar,
  BarChart,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
} from "recharts";
import { useMobileView } from "../../../common/utils";
import { Colors } from "../../../constants/colors";

const BarGraph = ({ data }) => (
  <ResponsiveContainer>
    <BarChart data={data}>
      <ReferenceLine y={0} stroke="#000" />
      <Tooltip wrapperStyle={{ fontSize: 13 }} />
      <Bar dataKey="totalAssets" fill={Colors.BLUE} />
      <Bar dataKey="longTermDebt" fill={Colors.ORANGE} />
      <XAxis dataKey="date" hide />
    </BarChart>
  </ResponsiveContainer>
);

const StyledRow = withStyles((theme) => ({
  root: {
    "&:nth-of-type(odd)": {
      backgroundColor: theme.palette.action.hover,
    },
  },
}))(TableRow);

export const BalanceSheet = ({ annualData, quarterData }) => {
  const isMobileView = useMobileView();

  return (
    <Box
      display="flex"
      mt={2}
      justifyContent="space-between"
      flexDirection={isMobileView ? "column" : "row"}
    >
      <TableContainer
        component={Paper}
        style={{ height: "fit-content", width: isMobileView ? "unset" : "60%" }}
      >
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Balance</TableCell>
              <TableCell>Assets</TableCell>
              <TableCell>Debt</TableCell>
              <TableCell>Year/Quarter</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {[...annualData, ...quarterData].map((ann, i) => (
              <StyledRow key={i}>
                <TableCell>{ann.balance}</TableCell>
                <TableCell>{ann.totalAssets}</TableCell>
                <TableCell>{ann.longTermDebt}</TableCell>
                <TableCell>{ann.date}</TableCell>
              </StyledRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      {isMobileView && <Box mt={3} />}
      <Box display="flex" flexGrow={1}>
        <Box
          display="flex"
          flexDirection="column"
          alignItems="center"
          flexGrow={1}
        >
          <Box width={160} flexGrow={1}>
            <BarGraph data={annualData} />
          </Box>
          <Typography variant="body2" style={{ opacity: 0.7 }}>
            <b>Annual</b>
          </Typography>
        </Box>

        <Box
          display="flex"
          flexDirection="column"
          alignItems="center"
          flexGrow={1}
        >
          <Box width={160} flexGrow={1}>
            <BarGraph data={quarterData} />
          </Box>
          <Typography variant="body2" style={{ opacity: 0.7 }}>
            <b>Quarter</b>
          </Typography>
        </Box>
      </Box>
    </Box>
  );
};
