import {
  Box,
  Divider,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  useTheme,
} from "@material-ui/core";
import {
  Cell,
  Pie,
  ResponsiveContainer,
  PieChart,
  Bar,
  BarChart,
  YAxis,
  XAxis,
  ReferenceLine,
  Tooltip,
} from "recharts";
import { Colors } from "../../../constants/colors";

const COLORS = ["#0088FE", "#FF8042", "#FFBB28"];

export const MarginPieChart = ({ data }) => (
  <Paper
    style={{
      padding: 25,
      borderRadius: 10,
      paddingBottom: 20,
      height: "fit-content",
    }}
    elevation={4}
    variant="outlined"
  >
    <Typography variant="h5">Margins</Typography>
    <Divider style={{ marginTop: 15 }} />
    <Box display="flex" flexDirection="column" mt={2}>
      <Box
        width={300}
        height={140}
        sx={{ fontFamily: useTheme().typography.fontFamily }}
      >
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} layout="vertical">
            <ReferenceLine x={0} stroke="#000" />
            <Tooltip wrapperStyle={{ fontSize: 13 }} />
            {/* <Bar dataKey="Gross profit" fill={Colors.ORANGE} />
            <Bar dataKey="Net profit" fill={Colors.GREEN_1} />
            <Bar dataKey="Operating Margin" fill={Colors.YELLOW} /> */}
            <Bar dataKey="value" />
            <YAxis type="category" dataKey="name" domain={["auto"]} hide />
            <XAxis type="number" hide />
          </BarChart>
        </ResponsiveContainer>
      </Box>
      <TableContainer component={Paper}>
        <Table size="small">
          <TableHead>
            <TableCell>Id</TableCell>
            <TableCell>Margin</TableCell>
            <TableCell>Value</TableCell>
          </TableHead>
          <TableBody>
            {data.map((itm) => (
              <TableRow key={itm.name}>
                <TableCell>
                  <Box
                    height={10}
                    width={10}
                    borderRadius={50}
                    bgcolor={itm.fill}
                  />
                </TableCell>
                <TableCell>{itm.name}</TableCell>
                <TableCell>{itm.value?.toFixed(3)}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  </Paper>
);
